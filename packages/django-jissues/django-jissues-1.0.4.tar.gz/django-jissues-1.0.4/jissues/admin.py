from zoneinfo import ZoneInfo
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpRequest
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from jissues.models import IssueBase
from jutil.format import format_timedelta, capfirst_lazy
from jutil.dates import get_date_range_by_name
from jutil.admin import ModelAdminBase, admin_log


class IssueStateListFilter(SimpleListFilter):
    title = _("state")
    parameter_name = "state-filter"
    lookup_choices = [
        (IssueBase.State.CLOSED, capfirst_lazy(_("issue.state.closed"))),
        ("-", _("All")),
    ]

    def lookups(self, request, model_admin):
        return self.lookup_choices

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string(remove=[self.parameter_name]),
            "display": _("issue.state.open"),
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string({self.parameter_name: lookup}),
                "display": title,
            }

    def queryset(self, request, queryset):
        val = self.value() or IssueBase.State.OPEN
        if val != "-":
            queryset = queryset.filter(state=val)
        return queryset


class IssueDueListFilter(SimpleListFilter):
    title = _("issue.due.label")
    parameter_name = "due-filter"
    lookup_options = [
        ("today", _("today")),
        ("tomorrow", _("tomorrow")),
        ("this_week", _("this week")),
        ("this_month", _("this month")),
        ("this_year", _("this year")),
        ("next_week", _("next week")),
        ("next_month", _("next month")),
    ]

    def lookups(self, request, model_admin):
        return self.lookup_options

    def get_user_timezone(self, user) -> str:  # noqa
        return settings.TIME_ZONE

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            begin, end = get_date_range_by_name(val, tz=ZoneInfo(self.get_user_timezone(request.user)))
            if val == "today":
                queryset = queryset.filter(due__lt=end)
            else:
                queryset = queryset.filter(due__gte=begin, due__lt=end)
        return queryset


class CommentInlineBase(admin.TabularInline):
    fields = [
        "created_brief",
        "text",
        "author",
    ]
    readonly_fields = [
        "created_brief",
        "author",
    ]
    min_num = 0
    extra = 1

    def has_change_permission(self, request, obj=None):
        if obj is not None and hasattr(obj, "id") and obj.id:
            return False
        return super().has_change_permission(request, obj)

    @admin.display(description=_("created"), ordering="created")  # type: ignore
    def created_brief(self, obj):
        return date_format(obj.created, "SHORT_DATE_FORMAT")


@admin.display(description=capfirst_lazy(_("assign.to.me.action")))  # type: ignore
def admin_assign_to_me(modeladmin, request, queryset):  # type: ignore
    user = request.user
    for obj in queryset.order_by("id").distinct():
        obj.assignee = user
        obj.save(update_fields=["assignee"])
        admin_log([obj], _("assignee") + f"= {user}", who=user)


@admin.display(description=capfirst_lazy(_("close.issue.action")))  # type: ignore
def admin_close_issue(modeladmin, request, queryset):  # type: ignore
    user = request.user
    for obj in queryset.exclude(state=IssueBase.State.CLOSED).order_by("id").distinct():
        obj.state = IssueBase.State.CLOSED
        obj.clean()
        obj.save()
        admin_log([obj], _("state") + " = " + _("issue.state.closed"), who=user)


@admin.display(description=capfirst_lazy(_("reopen.issue.action")))  # type: ignore
def admin_reopen_issue(modeladmin, request, queryset):  # type: ignore
    user = request.user
    for obj in queryset.exclude(state=IssueBase.State.OPEN).order_by("id").distinct():
        obj.state = IssueBase.State.OPEN
        obj.clean()
        obj.save()
        admin_log([obj], _("state") + " = " + _("issue.state.open"), who=user)


class LabelAdminBase(ModelAdminBase):
    save_on_top = False
    fields = [
        "name",
        "description",
        "color",
        "font_color",
        "as_html",
        "default",
    ]
    readonly_fields = [
        "as_html",
    ]
    search_fields = [
        "name",
    ]
    list_display = [
        "name",
        "description",
        "as_html",
        "default",
    ]

    @admin.display(description=_("color"), ordering="color")
    def as_html(self, obj):
        return obj.as_html()


class IssueAdminBase(ModelAdminBase):
    date_hierarchy = "created"
    fields = [
        "number",
        "state",
        "title",
        "body",
        "author",
        "assignee",
        "due",
        "closed",
        "created",
        "last_modified",
    ]
    readonly_fields = [
        "created",
        "last_modified",
        "closed",
        "author",
    ]
    list_display = [
        "summary",
        "assignee",
        "due_brief",
    ]
    list_filter = [
        IssueStateListFilter,
        IssueDueListFilter,
        ("author", admin.RelatedOnlyFieldListFilter),
        ("assignee", admin.RelatedOnlyFieldListFilter),
        "closed",
    ]
    actions = [
        admin_assign_to_me,
        admin_close_issue,
        admin_reopen_issue,
    ]
    autocomplete_fields = [
        "author",
        "assignee",
    ]

    @admin.display(description=_("issue.due.label"), ordering="due")
    def due_brief(self, obj):
        return date_format(obj.due, "SHORT_DATE_FORMAT") if obj.due else ""

    @admin.display(description=_("title"), ordering="title")
    def summary(self, obj):
        closed = obj.closed
        if closed:
            closed_str = date_format(closed, "SHORT_DATE_FORMAT")
            subheading = _("#{number} by {author} closed on {closed}").format(number=obj.number, closed=closed_str, author=obj.author or "-")
        else:
            created_ago = format_timedelta(now() - obj.created)
            subheading = _("#{number} opened {ago} ago by {author}").format(number=obj.number, ago=created_ago, author=obj.author or "-")
        labels = ""
        if hasattr(obj, "labels"):
            for label in obj.labels.all().order_by("name"):
                labels += str(label.as_html())
            labels = mark_safe(labels)
        return format_html(
            "{title} {labels}<br><span style='font-size:smaller; font-weight: 400;'>{subheading}</span>", title=obj.title, subheading=subheading, labels=labels
        )  # noqa

    def get_next_issue_number(self, request: HttpRequest) -> int:
        obj = self.get_queryset(request).order_by("-number").first()
        return obj.number + 1 if obj is not None else 1

    def get_changeform_initial_data(self, request: HttpRequest) -> dict[str, str | list[str]]:
        initial = super().get_changeform_initial_data(request)
        initial["number"] = self.get_next_issue_number(request)  # type: ignore
        return initial

    def save_form(self, request, form, change):
        instance = form.instance
        if hasattr(instance, "author") and instance.author is None:
            instance.author = request.user
        return form.save(commit=False)

    def save_formset(self, request, form, formset, change):
        for formset_form in formset:
            instance = formset_form.instance
            if hasattr(instance, "author") and instance.author is None:
                instance.author = request.user
        formset.save()
