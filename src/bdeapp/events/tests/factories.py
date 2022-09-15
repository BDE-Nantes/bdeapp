import factory

from bdeapp.events.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"event-{n}")
    date = factory.Faker("date")
    description = factory.Faker("text", max_nb_chars=85)
    long_description = factory.Faker("text", max_nb_chars=230)

    class Meta:
        model = Event
