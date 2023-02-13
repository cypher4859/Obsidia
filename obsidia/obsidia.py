import importlib
import os
import click

from exceptions import PluginException


CONTEXT_SETTINGS = dict(auto_envvar_prefix="OBSIDIA")
plugin_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "plugins"))

class Environment():
    def __init__(self) -> None:
        self.verbose = False

class ObsidiaCLI(click.MultiCommand):
    plugins = {}
    def list_commands(self, ctx):
        """List the available commands.

        Args:
            ctx (_type_): _description_
        """
        # Get all the plugins
        for filename in os.listdir(plugin_folder):
            if filename != "__pycache__":
                self.register_plugin(filename)
        
        return self.plugins

    def get_command(self, ctx, name):
        """Get a specific command.

        Args:
            ctx (_type_): _description_
            name (_type_): _description_
        """
        pass

    def register_plugin(self, filename):
        """Register a plugin with Obsidia.

        Args:
            filename (_type_): _description_
        """
        if filename not in self.plugins:
            mod = importlib.import_module(name=f"plugins.{filename}._lib", package="obsidia")
            self.plugins[filename] = getattr(mod, f"Obsidia{filename.capitalize()}Plugin")
            globals()[filename] = mod
        else:
            raise PluginException(f"Requested plugin is already registered; plugin-name={filename}")


@click.command(cls=ObsidiaCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enables verbose mode"
)
def cli(ctx, verbose, home):
    """Entrypoint for Obsidia"""
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home