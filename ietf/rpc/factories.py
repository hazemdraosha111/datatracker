# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-
import factory

from ietf.doc.factories import WgDraftFactory
from ietf.name.models import SourceFormatName, StdLevelName, StreamName, TlpBoilerplateChoiceName

from .models import Cluster, RfcToBe


class SourceFormatNameFactory(factory.django.DjangoModelFactory):
    slug = factory.Faker("word")
    name = factory.Faker("sentence")
    used = True

    class Meta:
        model = SourceFormatName


class TlpBoilerplateChoiceNameFactory(factory.django.DjangoModelFactory):
    slug = factory.Faker("word")
    name = factory.Faker("sentence")
    used = True

    class Meta:
        model = TlpBoilerplateChoiceName


class RpcToBeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RfcToBe

    draft = factory.SubFactory(WgDraftFactory)
    rfc_number = factory.Sequence(lambda n: n + 1000)
    submitted_format = factory.SubFactory(SourceFormatNameFactory)
    submitted_std_level = factory.LazyFunction(lambda: StdLevelName.objects.get(pk="ps"))
    submitted_boilerplate = factory.SubFactory(TlpBoilerplateChoiceNameFactory)
    submitted_stream = factory.LazyFunction(lambda: StreamName.objects.get(pk="ietf"))
    intended_std_level = factory.LazyAttribute(lambda o: o.submitted_std_level)
    intended_boilerplate = factory.LazyAttribute(lambda o: o.submitted_boilerplate)
    intended_stream = factory.LazyAttribute(lambda o: o.submitted_stream)


class AprilFirstRpcToBeFactory(RpcToBeFactory):
    is_april_first_rfc = True
    draft = None


class ClusterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cluster

    number = factory.Sequence(lambda n: n)
