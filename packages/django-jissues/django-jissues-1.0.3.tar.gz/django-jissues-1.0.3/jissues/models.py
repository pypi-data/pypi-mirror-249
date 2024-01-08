from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class LabelBase(models.Model):
    name = models.CharField(_("title"), max_length=64, db_index=True)
    description = models.TextField(_("description"), blank=True, default="")
    color = models.CharField(_("color"), max_length=64, default="white")
    font_color = models.CharField(_("font color"), max_length=64, default="black")
    default = models.BooleanField(_("default"), blank=True, db_index=True, default=False)

    class Meta:
        abstract = True
        verbose_name = _("issue.label.model.verbose.name")
        verbose_name_plural = _("issue.label.model.verbose.name.plural")

    def __str__(self):
        return str(self.name)

    def as_html(self) -> str:
        return format_html(
            "<span style='font-weight: 400; font-size: smaller; margin-left: 0.2em; margin-right: 0.2em; background-color:{}; color:{}; padding:0.25em 0.5em 0.25em 0.5em; border-radius: 1em;'>{}</span>",  # noqa
            self.color,
            self.font_color,
            self.name,
        )  # noqa


class CommentBase(models.Model):
    created = models.DateTimeField(_("created"), default=now, blank=True, db_index=True, editable=False)
    text = models.TextField(_("text"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"), on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        abstract = True
        verbose_name = _("issue.comment.model.verbose.name")
        verbose_name_plural = _("issue.comment.model.verbose.name.plural")


class IssueBase(models.Model):
    class State(models.TextChoices):
        OPEN = "O", _("issue.state.open")
        CLOSED = "C", _("issue.state.closed")

    number = models.IntegerField(_("number"), db_index=True)
    title = models.CharField(_("title"), max_length=128, db_index=True)
    state = models.CharField(_("state"), choices=State.choices, default=State.OPEN, max_length=1, db_index=True)
    due = models.DateField(_("issue.due.label"), blank=True, null=True, default=None, db_index=True)
    body = models.TextField(_("body"), blank=True, default="")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="issue_author_set",
        limit_choices_to={"is_staff": True},
    )  # noqa
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("assignee"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="issue_assignee_set",
        limit_choices_to={"is_staff": True},
    )  # noqa
    closed = models.DateTimeField(_("closed"), default=None, null=True, blank=True, db_index=True)
    created = models.DateTimeField(_("created"), default=now, blank=True, db_index=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), default=now, db_index=True, editable=False)

    class Meta:
        abstract = True
        verbose_name = _("issue.model.verbose.name")
        verbose_name_plural = _("issue.model.verbose.name.plural")

    def __str__(self):
        return f"{self.title} #{self.number}"

    @property
    def is_late(self) -> bool:
        return self.due and self.due < now().date()

    @property
    def is_due(self) -> bool:
        return self.due and self.due <= now().date()

    @property
    def is_closed(self) -> bool:
        return self.state == IssueBase.State.CLOSED

    @property
    def is_open(self) -> bool:
        return self.state == IssueBase.State.OPEN

    def clean(self):
        if self.closed is None:
            if self.is_closed:
                self.closed = now()
        elif self.is_open:
            self.closed = None
