import tw2.core as twc
import pep8bot.models
from sqlalchemy import and_


class UserProfile(twc.Widget):
    template = "mako:pep8bot.widgets.templates.profile"
    user = twc.Param("An instance of the User SQLAlchemy model.")
    resources = [
        twc.JSLink(filename="static/profile.js"),
    ]

    show_buttons = twc.Param("show my buttons?", default=False)

    def prepare(self):
        """ Query github for some information before display """

        # Try to refresh list of repos only if the user has none.
        if not self.user.all_repos:
            self.user.sync_repos()


    def make_button(self, kind, username, repo_name):
        # Just for reference
        unimplemented = ['pylint', 'pyflakes', 'mccabe']
        implemented = ['pep8']

        if kind in implemented:
            # TODO -- Can we use resource_url here?
            link = '/api/%s/%s/toggle?kind=%s' % (username, repo_name, kind)
            click = 'onclick="subscribe(\'%s\')"' % link
            Repo = pep8bot.models.Repo
            query = Repo.query.filter(and_(
                Repo.username==username, Repo.name==repo_name))

            repo = query.one()

            if getattr(repo, '%s_enabled' % kind):
                cls, text = "btn-success", "Disable"
            else:
                cls, text = "btn-danger", "Enable"

            return "<button id='%s-%s-%s' class='btn %s' %s>%s</button>" % (
                username, repo_name, kind, cls, click, text)
        else:
            return "<button class='btn btn-inverse'>N/A</button>"
