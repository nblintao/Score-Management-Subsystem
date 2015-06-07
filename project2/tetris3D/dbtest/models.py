from django.db import models

# Create your models here.
__author__ = 'skar'


from django.db import models


class TempTable(models.Model):
    faculty_id = models.CharField(max_length=6)
    student_id = models.CharField(max_length=10)
    class_id = models.CharField(max_length=8)
    ''' the above three should be modified to ForeignKey
        not sure if class_id is a primary of class_info
         in IMS
    '''
    score = models.FloatField()

    class Meta:
        ordering = ["faculty_id"]

    def __str__(self):
        return 'score of student %s in class %s' \
            % (self.student_id, self.class_id)


class MessageTable(models.Model):
    from_faculty_id = models.CharField(max_length=6)
    to_faculty_id = models.CharField(max_length=6)
    class_id = models.CharField(max_length=8)
    student_id = models.CharField(max_length=10)
    ''' foreignkey again '''
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ["from_faculty_id"]

    def __str__(self):
        return 'message on student %s, from faculty %s to %s' \
            % (self.student_id, self.from_faculty_id, self.to_faculty_id)


class ScoreTable(models.Model):
    class_id = models.CharField(max_length=8)
    student_id = models.CharField(max_length=10)

    score = models.FloatField()

    class Meta:
        ordering = ["class_id"]

    def __str__(self):
        return 'score of student %s in class %s' \
            % (self.student_id, self.class_id)

