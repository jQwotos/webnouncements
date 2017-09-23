# Webnouncements

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Webnouncements](#webnouncements)
	- [templating](#templating)
	- [Frontend](#frontend)
		- [Frameworks](#frameworks)
		- [Static ```static/```](#static-static)
		- [Templates ```templates/```](#templates-templates)
			- [Includes ```templates/_includes/```](#includes-templatesincludes)
			- [display ```templates/display/```](#display-templatesdisplay)
			- [manage ```templates/manage/```](#manage-templatesmanage)
			- [submit ```templates/submit/```](#submit-templatessubmit)
	- [Backend](#backend)
		- [lib ```lib/```](#lib-lib)
		- [apps ```lib/apps/```](#apps-libapps)
			- [supports ```lib/apps/supports```](#supports-libappssupports)
			- [```lib/apps/constants.py```](#libappsconstantspy)
			- [```lib/apps/dater.py```](#libappsdaterpy)
			- [```lib/apps/main.py```](#libappsmainpy)

<!-- /TOC -->

## templating
- We use the [jinja2 templating engine](http://jinja.pocoo.org/docs/2.9/) which uses the liquid templating language.
- Shopify has a [handy little cheat sheet](https://www.shopify.ca/partners/shopify-cheat-sheet) with most of the liquid templating syntax.

## Frontend
- Front end is the actual html, css and js that is used to make the website look like something nice.
### Frameworks
- Currently the [MaterializeCSS framework](materializecss.com) is used.
- Other front end frameworks can be added,
  - Just add them to the ```templates/_includes/head.html``` file and the rest of the pages that use the base template will also have them ready.

### Static ```static/```
- Static files do not perform any backend action, instead they are static content.

### Templates ```templates/```

#### Includes ```templates/_includes/```
- This folder contains html that is to be imported by templates, the head, navbar and scripts for the frontend frameworks are stored here.

#### display ```templates/display/```
- This folder contains all of the templates that relate to displaying announcements for the general public

  - ```display.html```
    - This file has the basic display that is to be iframed

  - ```print.html```
    - Template for creating a easily printable view

  - ```read.html```
    - The template that is the read announcements button

#### manage ```templates/manage/```
- Templates that relate admin related tasks
  - ```templates/manage/manage.html```
    - Displays all of the users, invite code generation, user removal for admin links only.

#### submit ```templates/submit/```
- Templates that

## Backend
### lib ```lib/```
- Contains all of the scripts that pertain to the backend of the webapp.
### apps ```lib/apps/```
- Contains all of the apps that are used to display and handle get and post requests.
#### supports ```lib/apps/supports```
- Scripts that are imported by apps that can handle multiple things, some store constants.
#### ```lib/apps/constants.py```
- Contains some variables that are used across multiple different scripts

#### ```lib/apps/dater.py```
- Contains the function that is used for submissions
    - ```poster(self, new = True):```
      takes in the self which is the

#### ```lib/apps/main.py```
- Main contains the primary Handler class which has uses the webapp2.RequestHandler class

  - ```class Handler():```

    - ```respondToJson(self, json_data):```
      - requires json data (in dictionary from)
      - sends json data to client

    - ```write(self, *a, **kw):```
      - basic without templating response to a get request in plain text.
    - ```render_str(self, template, **params)```
      - renders a template with the optional params
        - the params are passed to the template
