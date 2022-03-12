from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Information message about training."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        '''Return information about a completed excercise.'''
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Basic Training class."""
    M_IN_KM: int = 1000  # constant for converting from meters to kilometers
    LEN_STEP: float = 0.65  # step length in meters
    HOURS_IN_MINUTES = 60  # constant for conventing from hours to minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тraining: running."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM * self.duration * self.HOURS_IN_MINUTES)


class SportsWalking(Training):
    """Training: sportswalking."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.HOURS_IN_MINUTES)


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38  # stroke length in meters
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

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

    def get_mean_speed(self) -> float:
        '''Get average speed.'''
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        '''Return the number of calories burned.'''
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Read data from received sensors."""
    if workout_type not in ('SWM', 'RUN', 'WLK'):
        raise ValueError('Wrong workout_type')
    else:
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


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
