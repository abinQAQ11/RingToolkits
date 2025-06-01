import math
from . import Matrix
import numpy as np
from typing import Optional
# ----------------------------------------------------------------------------------------------------------------------
class Element(object):
    _tracked_attrs = {"length", "type", "k"}
    def __init__(self, family_name: str, length: float = 0.0, k: Optional[float] = 0.0):
        self.family_name = family_name
        self.length = length
        self.k = k
        self.slices = []
        self.type = "element"
        self.zoom = 1e10
        self.beta_0 = 0.0
        self.gamma_0 = 0.0
        self.b_rho = 0.0

    def __setattr__(self, name: str, value: object):
        if name in self._tracked_attrs:
            current = getattr(self, name, None)
            if current != value:
                super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def __str__(self) -> str:
        return (
            f"{self.type.capitalize()}:\n"
            f"\tFamName: {self.family_name}\n"
            f"\t Length: {self.length}"
        )
# ----------------------------------------------------------------------------------------------------------------------
class Drift(Element):
    def __init__(self, family_name: str, length: float = 0.0):
        super().__init__(family_name, length)
        self.type = "drift"

    @property
    def matrix(self):
        return Matrix.drift(self.length, self.beta_0, self.gamma_0)

    def create_slice(self, length: float,) -> dict:
        return {'l': length, 'name': self.family_name, 'type': self.type,
                'matrix': Matrix.drift(length, self.beta_0, self.gamma_0)}

    def slice(self, slice_length: float) -> None:
        self.slices = []
        t_l_s = round(self.length * self.zoom)        # t_l_s: total_length_scaled
        s_l_s = round(slice_length * self.zoom)       # s_l_a: slice_length_scaled
        num_slices, r_l_s = divmod(t_l_s, s_l_s)      # r_l_s: remnant_length_scaled
        s_l_a = s_l_s / self.zoom                     # s_l_a: slice_length_actual
        r_l_a = r_l_s / self.zoom                     # r_l_a: remnant_length_actual
        self.slices = [self.create_slice(s_l_a) for _ in range(num_slices)]
        if r_l_s > 0:
            self.slices.append(self.create_slice(r_l_a))
# ----------------------------------------------------------------------------------------------------------------------
class Sextupole(Element):
    def __init__(self, family_name: str, length: float, k: Optional[float] = 0.0):
        super().__init__(family_name, length, k)
        self.type = "sextupole"

    @property
    def matrix(self):
        return Matrix.sext(self.length, self.beta_0, self.gamma_0)

    def create_slice(self, length: float) -> dict:
        return {'l': length, 'k2': self.k, 'name': self.family_name, 'type': self.type,
                'matrix': Matrix.sext(length, self.beta_0, self.gamma_0)}

    def slice(self, slice_length: float) -> None:
        """A switch to decide whether to slice or not."""
        # slice_length = self.length
        self.slices = []
        t_l_s = round(self.length * self.zoom)
        s_l_s = round(slice_length * self.zoom)
        num_slices, r_l_s = divmod(t_l_s, s_l_s)
        s_l_a = s_l_s / self.zoom
        r_l_a = r_l_s / self.zoom
        self.slices = [self.create_slice(s_l_a) for _ in range(num_slices)]
        if r_l_s > 0.0:
            self.slices.append(self.create_slice(r_l_a))

    def __str__(self) -> str:
        return (
            super().__str__() +
            f"\n\t     K2: {self.k}"
        )
# ----------------------------------------------------------------------------------------------------------------------
class Quadrupole(Element):
    def __init__(self, family_name: str, length: float=0.0, k: Optional[float] = 0.0):
        super().__init__(family_name, length, k)
        self.type = "quadrupole"

    @property
    def matrix(self):
        return Matrix.quad(self.length, self.k, self.beta_0, self.gamma_0)

    def create_slice(self, length: float) -> dict:
        return {'l': length, 'k': self.k, 'name': self.family_name, 'type': self.type,
                'matrix': Matrix.quad(length, self.k, self.beta_0, self.gamma_0)}

    def slice(self, slice_length):
        self.slices = []
        t_l_s = round(self.length * self.zoom)
        s_l_s = round(slice_length * self.zoom)
        num_slices, r_l_s = divmod(t_l_s, s_l_s)
        s_l_a = s_l_s / self.zoom
        r_l_a = r_l_s / self.zoom
        self.slices = [self.create_slice(s_l_a) for _ in range(num_slices)]
        if r_l_s > 0.0:
            self.slices.append(self.create_slice(r_l_a))

    def __str__(self) -> str:
        return (
            super().__str__() +
            f"\n\t      K: {self.k}"
        )
# ----------------------------------------------------------------------------------------------------------------------
class Dipole(Element):
    _tracked_attrs = Element._tracked_attrs | {"bending_angle", "entrance_angle", "exit_angle"}
    def __init__(self, family_name: str,
                 length: float = 0.0,
                 k: Optional[float] = 0.0,
                 bending_angle: Optional[float] = 0.0,
                 entrance_angle: Optional[float] = 0.0,
                 exit_angle: Optional[float] = 0.0,
                 gap: Optional[float] = 0.0,
                 k1in: Optional[float] = 0.0,
                 k2in: Optional[float] = 0.0,
                 k1ex: Optional[float] = 0.0,
                 k2ex: Optional[float] = 0.0,):
        super().__init__(family_name, length, k)
        self.gap = gap
        self.k1in = k1in
        self.k1ex = k1ex
        self.k2in = k2in
        self.k2ex = k2ex
        self.bending_angle = math.radians(bending_angle)
        self.entrance_angle = math.radians(entrance_angle)
        self.exit_angle = math.radians(exit_angle)
        self.type = "bending"

    @property
    def B0(self):
        return self.b_rho / self.rho

    @property
    def rho(self):
        return self.length / self.bending_angle if self.bending_angle else 1

    @property
    def edge_left(self):
        return Matrix.edge(self.rho, self.entrance_angle, 0.0)

    @property
    def bend_middle(self):
        return Matrix.bend(self.length, self.k, self.rho, self.beta_0, self.gamma_0)

    @property
    def edge_right(self):
        return Matrix.edge(self.rho, 0.0, self.exit_angle)

    @property
    def matrix(self):
        return np.linalg.multi_dot([self.edge_right, self.bend_middle, self.edge_left])

    def slice(self, slice_length):
        self.slices = []
        t_l_s = round(self.length * self.zoom)
        s_l_s = round(slice_length * self.zoom)
        num_slices, r_l_s = divmod(t_l_s, s_l_s)
        s_l_a = s_l_s / self.zoom
        r_l_a = r_l_s / self.zoom

        for i in range(num_slices):
            slice_magnet = {'k': self.k, 'l': s_l_a, 'rho': self.rho, 'name': self.family_name, 'type': self.type}
            if i == 0:
                slice_magnet['t1'] = self.entrance_angle
                slice_magnet['t2'] = 0.0
                slice_magnet['matrix'] = np.dot(
                    Matrix.bend(slice_magnet['l'], slice_magnet['k'], slice_magnet['rho'], self.beta_0, self.gamma_0),
                    self.edge_left)
            elif i == num_slices - 1 and r_l_s == 0.0:
                slice_magnet['t1'] = 0.0
                slice_magnet['t2'] = self.exit_angle
                slice_magnet['matrix'] = np.dot(
                    self.edge_right,
                    Matrix.bend(slice_magnet['l'], slice_magnet['k'], slice_magnet['rho'], self.beta_0, self.gamma_0))
            else:
                slice_magnet['t1'] = slice_magnet['t2'] = 0.0
                slice_magnet['matrix'] = Matrix.bend(
                    slice_magnet['l'], slice_magnet['k'], slice_magnet['rho'], self.beta_0, self.gamma_0)
            self.slices.append(slice_magnet)
        if r_l_s > 0.0:
            slice_magnet = {'k': self.k, 'l': r_l_a, 'rho': self.rho,
                            't1': 0.0, 't2': self.exit_angle, 'name': self.family_name, 'type': self.type}
            slice_magnet['matrix'] = np.dot(
                self.edge_right,
                Matrix.bend(slice_magnet['l'], slice_magnet['k'], slice_magnet['rho'], self.beta_0, self.gamma_0))
            self.slices.append(slice_magnet)

    def __str__(self):
        return (f"Dipole:\n"
                f"\t      FamName: {self.family_name}\n"
                f"\t       Length: {self.length}\n"
                f"\t BendingAngle: {self.bending_angle}\n"
                f"\tEntranceAngle: {self.entrance_angle}\n"
                f"\t    ExitAngle: {self.exit_angle}\n"
                f"\t            K: {self.k}")
# ----------------------------------------------------------------------------------------------------------------------
class Octupole(Element):
    def __init__(self, family_name: str, k: float, length: Optional[float] = 0.0):
        super().__init__(family_name, length, k)
        self.type = "octupole"

    @property
    def matrix(self):
        return Matrix.oct()

    def __str__(self) -> str:
        return (
            super().__str__() +
            f"\n\t      K: {self.k}"
        )
# ----------------------------------------------------------------------------------------------------------------------
class Solenoid(Element):
    def __init__(self, family_name: str, k: float):
        super().__init__(family_name, k)
        self.type = "solenoid"

    @property
    def matrix(self):
        return Matrix.solenoid(self.length, self.k, self.beta_0, self.gamma_0)

    def __str__(self) -> str:
        return (
            super().__str__() +
            f"\n\t      B0: {self.k}"
        )
# ----------------------------------------------------------------------------------------------------------------------