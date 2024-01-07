import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from vgscli.cli import create_account_mgmt_api, create_vault_mgmt_api
from vgscli.cli_utils import dump_camelized_yaml, read_file
from vgscli.errors import handle_errors


@with_plugins(iter_entry_points("vgs.generate.plugins"))
@click.group("generate")
def generate() -> None:
    """
    Output a VGS resource template. Edited templates can be applied with a
    corresponding command.
    """
    pass


@generate.command("vault")
@handle_errors()
def generate_vault() -> None:
    """
    Output a vault template.
    """
    click.echo(read_file("resource-templates/vault-template.yaml"), nl=False)


@generate.command("access-credentials")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors()
def generate_access_credentials(ctx, vault):
    """
    Generate a VGS access-credential
    """
    account_mgmt = create_account_mgmt_api(ctx)

    response = account_mgmt.vaults.get_by_id(vault)

    vault_mgmt = create_vault_mgmt_api(
        ctx, response.body["data"][0]["links"]["vault_management_api"]
    )

    response = vault_mgmt.credentials.create(headers={"VGS-Tenant": vault})

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "AccessCredentials",
                "data": response.body["data"],
            }
        )
    )


@generate.command("http-route")
@handle_errors()
def generate_route():
    """
    Generate a VGS HTTP Route
    """
    click.echo(read_file("resource-templates/http-route-template.yaml"), nl=False)


@generate.command("mft-route")
@handle_errors()
def generate_route():
    """
    Generate a VGS MFT Route
    """
    click.echo(read_file("resource-templates/mft-route-template.yaml"), nl=False)
