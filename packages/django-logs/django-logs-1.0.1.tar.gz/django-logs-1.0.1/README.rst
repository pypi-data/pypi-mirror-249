============================
django-logs
============================

Tracking changes to django models.


* Model fields for keeping track of the user and session that created and modified a model instance.
* Abstract model class with fields ``created_by`` and ``modified_by`` fields.
* A model manager class that can automatically track changes made to a model in the database.


Quickstart Guide
===============================

Install it with pip from PyPi::

    pip install django-logs

Add ``logs.middleware.UserLoggingMiddleware`` to your ``MIDDLEWARE_CLASSES``::


    MIDDLEWARE_CLASSES = (
        ...
        'logs.middleware.UserLoggingMiddleware',
    )


To just track who created or edited a model instance just make it inherit from ``AuthStampedModel``::


    from logs.models import AuthStampedModel

    class WarehouseEntry(AuthStampedModel):
        product = models.ForeignKey(Product)
        quantity = models.DecimalField(max_digits = 10, decimal_places = 2)


This will add 4 fields to the ``WarehouseEntry`` model:

* ``created_by`` - A foreign key to the user that created the model instance.
* ``created_with_session_key`` - Stores the session key with which the model instance was first created.
* ``modified_by`` - A foreign key to the user that last saved a model instance.
* ``modified_with_session_key`` - Stores the session key with which the model instance was last saved.

If you want to track full model change history you need to attach an ``AuditLog`` manager to the model::

    from django.db import models
    from logs.models.fields import LastUserField
    from logs.models.managers import AuditLog


    class ProductCategory(models.Model):
        name = models.CharField(max_length=150, primary_key = True)
        description = models.TextField()

        logs = AuditLog()

    class Product(models.Model):
        name = models.CharField(max_length = 150)
        description = models.TextField()
        price = models.DecimalField(max_digits = 10, decimal_places = 2)
        category = models.ForeignKey(ProductCategory)

        logs = AuditLog()

You can then query the audit log::

    In [2]: Product.logs.all()
    Out[2]: [<ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:29.292363>,
            <ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:24.898991>,
            <ProductAuditLogEntry: Product: My Gadget super changed at 2011-02-25 06:04:15.448934>,
            <ProductAuditLogEntry: Product: My Gadget changed at 2011-02-25 06:04:06.566589>,
            <ProductAuditLogEntry: Product: My Gadget created at 2011-02-25 06:03:57.751222>,
            <ProductAuditLogEntry: Product: My widget created at 2011-02-25 06:03:42.027220>]