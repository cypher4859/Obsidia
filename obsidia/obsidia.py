import os
import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix="OBSIDIA")
plugin_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "plugins"))

class Environment():
    def __init__(self) -> None:
        self.verbose = False

class ObsidiaCLI(click.MultiCommand):
    def list_commands(self, ctx):
        """List the available commands.

        Args:
            ctx (_type_): _description_
        """
        plugins = []
        # Get all the plugins
        for filename in os.listdir(plugin_folder):
            plugins.append(filename)
        
        plugins.sort()
        return plugins

    def get_command(self, ctx, name):
        """Get a specific command.

        Args:
            ctx (_type_): _description_
            name (_type_): _description_
        """
        pass

@click.command(cls=ObsidiaCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enables verbose mode"
)
def cli(ctx, verbose, home):
    """Entrypoint for Obsidia

    Args:
        ctx (_type_): _description_
        verbose (_type_): _description_
        home (_type_): _description_
    """
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home