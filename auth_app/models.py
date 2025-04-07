from django.db import models
import bcrypt

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Hash password on creation
            self.password = bcrypt.hashpw(
                self.password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
        super(Store, self).save(*args, **kwargs)

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password.encode('utf-8')
        )

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Hash password on creation
            self.password = bcrypt.hashpw(
                self.password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
        super(Customer, self).save(*args, **kwargs)

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password.encode('utf-8')
        )