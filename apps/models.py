from django.db import models
from django.utils.translation import gettext_lazy as _

class TestTopic(models.Model):
    title = models.CharField(
    _("Название или тема тестов"),max_length=64, help_text=_('Введите название теста')
)
    description = models.TextField(_("Текст"),help_text=_('Введите описание или тему текста'))

    def __str__(self):
        return self.title

class Question(models.Model):
    topic = models.ForeignKey(TestTopic, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(_('Вопрос'),help_text=_('Введите вопрос'))

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(_('Ответ'),max_length=255,help_text=_('Введите ответ'))
    is_correct = models.BooleanField(_('Правильный ответ'),default=False,help_text=_('Выберите правильный ответ'))

    def __str__(self):
        return self.text
