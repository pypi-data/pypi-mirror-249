import yaml
import os
import click
from bs4 import BeautifulSoup
from shutil import copy2

class DefaultHelp(click.Command):
    def __init__(self, *args, **kwargs):
        context_settings = kwargs.setdefault('context_settings', {})
        if 'help_option_names' not in context_settings:
            context_settings['help_option_names'] = ['-h', '--help']
        self.help_flag = context_settings['help_option_names'][0]
        super(DefaultHelp, self).__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        if not args:
            args = [self.help_flag]
        return super(DefaultHelp, self).parse_args(ctx, args)

@click.command(cls=DefaultHelp)
@click.option("--init", help="Initialize the repos as Git submodules.", is_flag=True, show_default=True)
@click.option("--update", help="Update the repos, i.e., the Git submodules.", is_flag=True, show_default=True)
@click.option("--build", help="Build all MkDocs projects and generate the landing page.", is_flag=True, show_default=True)

def cli(init, update, build):

    config = loadConfig()

    if init:
        # Initialize the repos as Git submodules
        click.echo("Adding submodules ...")
        cwd = os.path.abspath(os.getcwd())
        for repo in config["repos"]:
            # Add repo as git submodule
            repo_dir = os.path.abspath(config["repos_dir"] + os.path.sep + repo["name"])
            os.system("git -c http.sslVerify=false submodule add " + repo["url"] + " " + repo_dir)
            if "branch" in repo:
              repo_branch = repo["branch"]
              click.echo("Using branch " + repo_branch + " in repository " + repo_dir)
              os.chdir(repo_dir)
              os.system("git checkout " + repo_branch)
              os.chdir(cwd)
        click.echo("Done.")

    if update:
        # Update the repos, i.e., the Git submodules
        click.echo("Updating submodules ...")
        os.system("git -c http.sslVerify=false submodule update")
        click.echo("Done.")

    if build:
        # Build MkDocs projects
        # Copy image files and build projects
        click.echo("Building projects ...")
        cwd = os.path.abspath(os.getcwd())
        for repo in config["repos"]:
            repo_dir = os.path.abspath(config["repos_dir"] + os.path.sep + repo["name"])
            if not "mkdocs_dir" in repo:
                repo["mkdocs_dir"] = "."
            if not "mkdocs_config" in repo:
                repo["mkdocs_config"] = "mkdocs.yml"
            

            repo_target_image = os.path.abspath(config["target_dir"] + os.path.sep + repo["image"])
            os.makedirs(os.path.dirname(repo_target_image), exist_ok=True)
            copy2(repo["image"], repo_target_image)

            repo_site_dir = os.path.abspath(config["target_dir"] + os.path.sep + repo["name"])
            os.chdir(repo_dir + os.path.sep + repo["mkdocs_dir"])
            os.system("mkdocs build --config-file " + repo["mkdocs_config"] + " --site-dir " + repo_site_dir)
            os.chdir(cwd)

        # Copy extra files
        if "extra_files" in config:
            click.echo("Copying extra files ...")
            for extrafile in config["extra_files"]:
                os.makedirs(os.path.dirname(config["target_dir"] + os.path.sep + extrafile), exist_ok=True)
                copy2(extrafile, config["target_dir"] + os.path.sep + extrafile)

        # Generate index.html based on template
        click.echo("Generating landing page ...")
        soup = loadTemplate(config["index_tpl"])
        # Add unordered list as child of element_id
        element = soup.find(id=config["element_id"])
        if element.ul is None:
            element.insert(1, soup.new_tag("ul"))
        for repo in config["repos"]:
            # Add a list item for each repo
            index_html = "index.html"

            repo_element = element
            if "element_id" in repo:
                repo_element = soup.find(id=repo["element_id"])
                if repo_element.ul is None:
                    repo_element.insert(1, soup.new_tag("ul"))

            if "index_html" in repo:
                index_html = repo["index_html"]

            list_tag = soup.new_tag("li")
            anchor_tag = soup.new_tag("a", href=repo["name"] + "/" + index_html)
            image_tag = soup.new_tag("img", src=repo["image"])
            heading_tag = soup.new_tag("span")
            heading_tag.string = repo["title"]

            anchor_tag.insert(1, image_tag)
            anchor_tag.insert(1, heading_tag)
            list_tag.insert(1, anchor_tag)

            if "pdf" in repo:
                a_tag = soup.new_tag("a", href=repo["name"] + "/" + repo["pdf"])
                a_tag.string = 'pdf'
                list_tag.insert(1, a_tag)

            repo_element.ul.insert(1, list_tag)

        # Write index.html
        with open(config["target_dir"] + "/index.html", "w", encoding="utf8") as htmlfile:
            htmlfile.write(str(soup))
            htmlfile.close()
        click.echo("Done.")

def loadConfig():
    configfile = open(r'config.yml')
    try:
        config = yaml.safe_load(configfile)
        # Set defaults
        if not "repos_dir" in config:
            config["repos_dir"] = os.getcwd()
        if not "target_dir" in config:
            config["target_dir"] = "site"
        if not "element_id" in config:
            config["element_id"] = "multirepo" 
        if not "index_tpl" in config:
            config["index_tpl"] = "index.tpl" 

    finally:
        configfile.close()
    return config

def loadTemplate(index_file):
    templatefile = open(index_file)
    try:
        contents = yaml.safe_load(templatefile)
        soup = BeautifulSoup(contents, 'html.parser')
    finally:
        templatefile.close()
    return soup
