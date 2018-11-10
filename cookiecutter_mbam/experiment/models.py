# -*- coding: utf-8 -*-
"""Experiment model."""

from cookiecutter_mbam.extensions import db
from cookiecutter_mbam.user import User, Role
from sqlalchemy import event
from cookiecutter_mbam.database import Column, Model, SurrogatePK, db, reference_col, relationship

from flask import current_app

def debug():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"

class Experiment(SurrogatePK, Model):
    """A user's experiment, during which they are scanned."""

    __tablename__ = 'experiments'
    date = Column(db.Date(), nullable=False)
    scanner = Column(db.String(80), nullable=True)
    num_scans = Column(db.Integer(), nullable=True, default=0)
    xnat_experiment_id = Column(db.String(80), nullable=True)
    #user = relationship('User', backref='experiments')
    user_id = reference_col('users', nullable=True)


    def __init__(self, date, scanner, num_scans, user_id, **kwargs):
        """Create instance."""
        db.Model.__init__(self, date=date, scanner=scanner, user_id=user_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Experiment({date})>'.format(date=self.date)

#
# def update_user_exp_count(mapper, connection, target):
#     db.session.begin_nested()
#     user_id = target.user_id
#     print("user id is ", user_id)
#     user = User.get_by_id(user_id)
#     user.update(num_experiments=user.num_experiments + 1)
#     print("This is my listener.  user.num experiments is", user.num_experiments)
#
# #
# event.listen(Experiment, 'before_insert', update_user_exp_count)


