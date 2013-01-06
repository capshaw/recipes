# A Recipe Server
### A toy python server for hosting and serving recipes

This is a simple (toy) python server for hosting recipes. Pages are compiled upon request through JSON data embedded into HTML templates. All of this is done with Jinja, a templating library for python. All recipes are available at `localhost/name-of-recipe` where `name-of-recipe` is a file on the system named `recipes/name-of-recipe.json`.

(As a note, `localhost/name-of-recipe.json` is valid and will respond with a json object to the browser)

## To Use

Simply run `server.py`. You'll probably need root credentials. Visit `localhost` with your browser of choice to see a list of recipes.

## To Add Recipes

Put a json file representing the recipe in the recipes folder. Note the existing JSON recipes' syntax.