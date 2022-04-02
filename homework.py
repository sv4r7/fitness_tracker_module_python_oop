from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    FINAL_MESSAGE = ('Тип тренировки: {training_type}; '
                     'Длительность: {duration:.3f} ч.; '
                     'Дистанция: {distance:.3f} км; '
                     'Ср. скорость: {speed:.3f} км/ч; '
                     'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.FINAL_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    FROM_HOURS_TO_MINUTES_CONVERT: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist: float = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Идет вызов пустого метода '
                                  'родительского класса')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        MEAN_SPEED_RUNNING_MULTIPLIER: int = 18
        MEAN_SPEED_RUNNING_DEDUCTIBLE: int = 20

        calories_run: float = ((MEAN_SPEED_RUNNING_MULTIPLIER
                               * self.get_mean_speed()
                               - MEAN_SPEED_RUNNING_DEDUCTIBLE)
                               * self.weight / self.M_IN_KM * self.duration
                               * self.FROM_HOURS_TO_MINUTES_CONVERT)
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        MEAN_SPEED_SPORTS_WALKING_WEIGHT_MULT_ONE: float = 0.035
        MEAN_SPEED_SPORTS_WALKING_WEIGHT_MULT_TWO: float = 0.029

        calories_walk: float = (((MEAN_SPEED_SPORTS_WALKING_WEIGHT_MULT_ONE
                                * self.weight + (self.get_mean_speed()
                                 ** 2 // self.height)
                                 * MEAN_SPEED_SPORTS_WALKING_WEIGHT_MULT_TWO
                                 * self.weight)
                                 * self.duration
                                 * self.FROM_HOURS_TO_MINUTES_CONVERT))
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        swim_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return swim_speed

    def get_spent_calories(self) -> float:
        SWIMMING_MEAN_SPEED_ADDITION_FACTOR: float = 1.1
        SWIMMING_WEIGHT_MULTIPLIER: int = 2
        swim_calories: float = ((self.get_mean_speed()
                                + SWIMMING_MEAN_SPEED_ADDITION_FACTOR)
                                * SWIMMING_WEIGHT_MULTIPLIER
                                * self.weight)
        return swim_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types_pack: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                      'RUN': Running,
                                                      'WLK': SportsWalking
                                                      }
    if workout_type not in training_types_pack:
        raise ValueError(f'Неизвестный тип тренировки {workout_type}')
    training_type: Type[Training] = training_types_pack[workout_type]
    return training_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
