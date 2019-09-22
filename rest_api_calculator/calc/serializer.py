from rest_framework import serializers

arithmetic_choices = [('add', 'Addition'),
                      ('sub', 'Subtraction'),
                      ('mul', 'Multiplication'),
                      ('div', 'Division'),
                      ('pow', 'Power'),
                      ('fact', 'Factorial'),
                      ('sqrt', 'SquareRoot')]


class CalcSerializer(serializers.Serializer):
    op = serializers.ChoiceField(choices=arithmetic_choices)
    a = serializers.DecimalField(max_digits=19, decimal_places=10, coerce_to_string=False)
    b = serializers.DecimalField(max_digits=19, decimal_places=10, coerce_to_string=False)
