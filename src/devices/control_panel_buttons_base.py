"""Abstract button callbacks for control panel UI."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ControlPanelButtonCallbacks(ABC):
    """Defines abstract button handlers used by the UI."""

    @abstractmethod
    def button1(self):
        pass

    @abstractmethod
    def button2(self):
        pass

    @abstractmethod
    def button3(self):
        pass

    @abstractmethod
    def button4(self):
        pass

    @abstractmethod
    def button5(self):
        pass

    @abstractmethod
    def button6(self):
        pass

    @abstractmethod
    def button7(self):
        pass

    @abstractmethod
    def button8(self):
        pass

    @abstractmethod
    def button9(self):
        pass

    @abstractmethod
    def button_star(self):
        pass

    @abstractmethod
    def button0(self):
        pass

    @abstractmethod
    def button_sharp(self):
        pass






