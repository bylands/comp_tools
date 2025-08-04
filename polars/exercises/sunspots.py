import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo  # noqa: INP001
    import polars as pl

    return mo, pl


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Sunspots
        The number of sunspots (darker regions on the surface of the sun that are colder than the surrounding area) varies over time with a roughly 11-year solar cycle.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        #### Import Data
        The file *sunspot_data.csv* contains data going back to 1818. For days without a reported number, the column *Number of Sunspots" contains the value -1.
    
        Make yourself familiar with the structure of the dataframe find the number of sunspots on your birthday and the maximum number of sunspots in the dataset.
        """
    )
    return


@app.cell
def _(mo, pl):
    path = 'exercises/data/sunspot_data.csv'

    sunspots = pl.read_csv(path)

    b_year = 1971
    b_month = 3
    b_day = 13

    birthday_spots = (sunspots.filter(
        (pl.col('Year') == b_year) &
        (pl.col('Month') == b_month) &
        (pl.col('Day') == b_day),
    )
     .get_column('Number of Sunspots').to_list()
    )[0]

    mo.md(
        f'''
        Number of objects in dataset: {sunspots.shape[0]}

        The number of sunspots on {b_day}/{b_month}/{b_year} was {birthday_spots}
        ''',
    )

    return (sunspots,)


@app.cell
def _(mo):
    mo.md(
        r"""
        #### Solar Cycle
        To verify the solar cycle, make a diagram showing the average number of sunspots per month. Ignore days with no observation.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        #### Method 1
        Create a column 'Year/Month' combining the year and month. You have to format single digit months with a leading zero.
        """
    )
    return


@app.cell
def _(pl, sunspots):
    def format_month(m):
        return f'{m:02d}'

    data = (sunspots
        .filter(pl.col('Number of Sunspots') != -1)
        .with_columns((pl.col('Year')+pl.col('Month')/12).alias('Year/Month'))
        .group_by('Year/Month')
        .agg(pl.col('Number of Sunspots').mean())
        .sort('Year/Month')
    )
    return (data,)


@app.cell
def _(data):
    data.plot.line(
        x='Year/Month',
        y='Number of Sunspots',
    )
    return


@app.cell
def _(mo):
    mo.md(r"As can be seen, there are 18 maxima between 1825 and 2025, which corresponds to a cycle of about 11 years.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        #### Method 2
        Use the built-in method pl.date to convert the date to a date dtype. Use the method group_by_dynamic to downsample the data to monthly intervals.
        """
    )
    return


@app.cell
def _(pl, sunspots):
    data2 = (sunspots
        .filter(pl.col('Number of Sunspots') != -1)
        .with_columns(pl.date(pl.col('Year'), pl.col('Month'), pl.col('Day')).alias('Date'))
        .group_by_dynamic('Date', every='1mo')
        .agg(pl.col('Number of Sunspots').mean())
    )
    return (data2,)


@app.cell
def _(data2):
    data2.plot.line(
        x='Date',
        y='Number of Sunspots',
    )
    return


@app.cell
def _(mo):
    mo.md(r"Method 2 has the advantage, that the interval can easily be adjusted, e.g. to 3 months.")
    return


if __name__ == "__main__":
    app.run()
