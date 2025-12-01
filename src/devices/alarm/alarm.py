from typing import List


class Alarm:
    """알람 클래스"""

    def __init__(self, alarm_id: int, xCoord: int = 0, yCoord: int = 0):
        """
        알람을 초기화합니다.

        Args:
            alarm_id: 알람 ID
            xCoord: 알람의 X 좌표
            yCoord: 알람의 Y 좌표
        """
        self.id = alarm_id
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.status = False  # False: 꺼짐, True: 울림

    def starting(self, alarm_id: int) -> bool:
        """
        알람을 시작합니다.

        Args:
            alarm_id: 시작할 알람 ID

        Returns:
            시작 성공 여부
        """
        if alarm_id == self.id:
            self.status = True
            return True
        return False

    def ending(self, alarm_id: int) -> bool:
        """
        알람을 종료합니다.

        Args:
            alarm_id: 종료할 알람 ID

        Returns:
            종료 성공 여부
        """
        if alarm_id == self.id:
            self.status = False
            return True
        return False

    def getLocation(self) -> List[int]:
        """
        알람의 위치를 반환합니다.

        Returns:
            알람 위치 [x, y]
        """
        return [self.xCoord, self.yCoord]

    def isRinging(self) -> bool:
        """
        알람이 울리고 있는지 확인합니다.

        Returns:
            알람 울림 여부
        """
        return self.status

    def ring(self, statusValue: bool) -> None:
        """
        알람 상태를 설정합니다.

        Args:
            statusValue: 설정할 알람 상태 (True: 울림, False: 꺼짐)
        """
        self.status = statusValue

    def setLocation(self, xCoord: int, yCoord: int) -> None:
        """
        알람의 위치를 설정합니다.

        Args:
            xCoord: X 좌표
            yCoord: Y 좌표
        """
        self.xCoord = xCoord
        self.yCoord = yCoord

    def getID(self) -> int:
        """
        알람 ID를 반환합니다.

        Returns:
            알람 ID
        """
        return self.id
