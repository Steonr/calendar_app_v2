"""
Explanation of the Value Object:

Value Objects are one of the building blocks of Domain Driven Design (DDD). 
It represents a value that doesn’t have identity and is immutable. When we compare two value objects, we are comparing their values, not their identities. For instance, if we compare two Money objects, we are comparing if each one values five dollars, not if they are the same five dollar bill.
Value objects also provide context. It means that a Money Value Object not only has the number five, but also the currency US dollar.
One of the main advantages of using Value Objects is that we can centralize the type definition and validation on the Value Object definition.
It is not mandatory to use Value Objects with the Clean Architecture but it may be a good idea. 
"""

import uuid

ShiftId = uuid.UUID