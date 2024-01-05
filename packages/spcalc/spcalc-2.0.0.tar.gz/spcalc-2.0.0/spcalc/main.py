# command line tool using click
from spcalc.calculator import Calculator
from spcalc.add import Add
from spcalc.subtract import Subtract
from spcalc.multiply import Multiply
from spcalc.divide import Divide
import click

operations = {
    "add": Add(),
    "subtract": Subtract(),
    "multiply": Multiply(),
    "divide": Divide(),
}


@click.command()
@click.option(
    "--num1",
    "-n1",
    default=0,
    help="First number",
    prompt="Enter first number",
    type=float,
)
@click.option(
    "--num2",
    "-n2",
    default=0,
    help="Second number",
    prompt="Enter second number",
    type=float,
)
@click.option(
    "--operation",
    "-op",
    default="add",
    type=click.Choice(operations.keys()),
    help="Operation to perform",
    prompt="Enter operation",
)
def main(num1, num2, operation):
    click.echo(
        click.style(
            "Running calculator...", blink=True, bg="black", fg="white", bold=True
        )
    )
    click.echo(click.style("=" * 50, fg="cyan"))

    calc = Calculator(num1, num2, operations[operation])
    # catch zero division error
    try:
        result = calc.execute()
    except ZeroDivisionError:
        click.echo(click.style("Cannot divide by zero", fg="red"))
        return
    except Exception:  # pylint: disable=broad-except
        click.echo(click.style("Something went wrong", fg="red"))
        return

    click.echo(
        click.style("Number 1: ", fg="cyan") + click.style(str(num1), fg="yellow")
    )

    click.echo(
        click.style("Number 2: ", fg="cyan") + click.style(str(num2), fg="yellow")
    )

    click.echo(
        click.style("Operation: ", fg="cyan") + click.style(operation, fg="green")
    )

    click.echo(click.style("=" * 50, fg="cyan"))

    click.echo(
        click.style("Result: ", fg="cyan")
        + click.style(str(result), fg="blue", bold=True)
    )

    click.echo(click.style("=" * 50, fg="cyan"))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
