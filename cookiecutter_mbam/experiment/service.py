from .models import Experiment

class ExperimentService:

    def add(self, user, date, scanner, num_scans):
        exp = Experiment.create(date=date, scanner=scanner, num_scans=num_scans, user_id=user.id)
        user.update(num_experiments=user.num_experiments + 1)
        print("here I am in the add function. user.num_experiments is ", user.num_experiments)
        return exp

        # todo: make sure deleting an experiment decrements this count