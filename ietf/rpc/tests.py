# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-
from django.db import transaction
from django.test import TestCase

from .factories import ClusterFactory, RpcToBeFactory

class ClusterTests(TestCase):
    def test_cluster_history(self):
        rtb = RpcToBeFactory.create_batch(3)
        cluster = ClusterFactory()
        
        rtb[0].cluster = cluster
        rtb[0].order_in_cluster = 1
        rtb[0].save()
        
        rtb[1].cluster = cluster
        rtb[1].order_in_cluster = 2
        rtb[1].save()
        
        rtb[2].cluster = cluster
        rtb[2].order_in_cluster = 3
        rtb[2].save()
        
        self.assertCountEqual(cluster.rfctobe_set.all(), rtb)

        with transaction.atomic():
            rtb[0].order_in_cluster = 3    
            rtb[0].save()
            rtb[2].order_in_cluster = 1
            rtb[2].save()
        
        with transaction.atomic():
            rtb[0].order_in_cluster = 2
            rtb[0].save()
            rtb[1].order_in_cluster = 1
            rtb[1].save()
            rtb[2].cluster = None
            rtb[2].save()
            
        changes = cluster.membership_changes()
        self.assertEqual(len(changes), 8)  # failing - once rtb[2] is not in our set, we're not seeing its change events
        self.assertCountEqual(cluster.history.as_of(changes[0]).rfctobe_set.all(), [rtb[0]])
        self.assertCountEqual(cluster.history.as_of(changes[1]).rfctobe_set.all(), [rtb[0], rtb[1]])
        self.assertCountEqual(cluster.history.as_of(changes[2]).rfctobe_set.all(), rtb)
        self.assertCountEqual(cluster.history.as_of(changes[3]).rfctobe_set.all(), rtb)
        self.assertCountEqual(cluster.history.as_of(changes[4]).rfctobe_set.all(), rtb)
        self.assertCountEqual(cluster.history.as_of(changes[5]).rfctobe_set.all(), rtb)
        self.assertCountEqual(cluster.history.as_of(changes[6]).rfctobe_set.all(), rtb)
        self.assertCountEqual(cluster.history.as_of(changes[7]).rfctobe_set.all(), [rtb[0], rtb[1]])
