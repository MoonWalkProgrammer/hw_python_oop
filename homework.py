from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Information message about training."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        '''Return information about a completed excercise.'''
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    pass


class Training:
    """Basic Training class."""
    M_IN_KM: int = 1000  # constant for converting from meters to kilometers
    LEN_STEP: float = 0.65  # step length in meters
    training_type: str = 'Running'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Return the number of calories burned."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return training information message."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
    pass


class Running(Training):
    """Тraining: running."""
    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        coeff_calorie_1: float = 18
        coeff_calorie_2: float = 20
        duration_in_minutes: float = self.duration * 60
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM * duration_in_minutes)
    pass


class SportsWalking(Training):
    """Training: sportswalking."""
    training_type: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        pass

    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        duration_in_minutes = self.duration * 60
        return ((coeff_calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * coeff_calorie_2 * self.weight) * duration_in_minutes)
    pass


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38  # stroke length in meters
    training_type: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        pass

    def get_mean_speed(self) -> float:
        '''Get average speed.'''
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Read data from received sensors."""
    training_dict: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    current_sport: Training = training_dict[workout_type]
    return current_sport(*data)


def main(training: Training) -> None:
    """Main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
