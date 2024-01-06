from typing import Annotated

import typer

from instagraper import scraper

app = typer.Typer()


@app.command()
def scrape(
    username: Annotated[str, typer.Argument(help="The instagram username")],
    x_ig_app_id: Annotated[
        str,
        typer.Option(
            help="Instagram app id (x-ig-app-id) header to authenticate the requests. If not provided, the tool will try to read it from the environment variable X_IG_APP_ID",
        ),
    ] = None,
    session_id: Annotated[
        str,
        typer.Option(
            help="Instagram session id (sessionid) cookie to authenticate the requests. If not provided, the tool will try to read it from the environment variable SESSION_ID",
        ),
    ] = None,
    compact: Annotated[
        bool,
        typer.Option(
            "--compact", "-c", help="wether to compact the JSON output or not"
        ),
    ] = True,
    with_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="whether to dump the posts to a JSON file or not.",
        ),
    ] = False,
    with_geojson: Annotated[
        bool,
        typer.Option(
            "--geojson",
            "-g",
            help="whether to dump the posts to a GeoJSON file or not. If map is enabled, this will be enabled by default.",
        ),
    ] = False,
    with_map: Annotated[
        bool,
        typer.Option(
            "--map",
            "-m",
            help="whether to create a map with the posts or not. It will enable GeoJSON output by default.",
        ),
    ] = False,
    target: Annotated[
        str,
        typer.Option(
            "--target",
            "-t",
            help="the target path/directory to save the output files. Defaults to a directory with the instagram username as it's name, e.g ./{username}/",
        ),
    ] = None,
    with_images: Annotated[
        bool,
        typer.Option(
            "--images",
            "-i",
            help="whether to download post's images or not. The images will be saved in the target/images directory.",
        ),
    ] = False,
    static_url: Annotated[
        str,
        typer.Option(
            "--static-url",
            "-s",
            help="The static url/path where the target directory will be hosted. Used to serve the images for the geojson output. e.g. if https://example.com/instagraper/ images will be in https://example.com/instagraper/{target}/images/",
        ),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            "-l",
            help="The maximum number of posts to scrape. If not provided, all posts will be scraped.",
        ),
    ] = None,
):
    """
    Scrape Instagram profile posts and corresponding locations
    #"""
    scraper.scrape(
        username=username,
        x_ig_app_id=x_ig_app_id,
        session_id=session_id,
        compact=compact,
        with_json=with_json,
        with_geojson=with_geojson,
        with_map=with_map,
        target=target,
        with_images=with_images,
        static_url=static_url,
        limit=limit
    )
