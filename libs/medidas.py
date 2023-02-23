# Modulos Medidas.py
#
# Módulo Medidas.py com classe e sobrecarga de funções matemáticas
# para trabalhar com Medidas Físicas: Valor ± Incerteza
#
# Por Rudson R. Alves
# 01 de Dezembro de 2009
#
# medidas
# Copyright (C) 2010  Rudson R. Alves (rudsonalves[a]rra.etc.br)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import division

__lib_name__ = 'medidas.py'
__version__ = '1.2.2'

import math

pi = math.pi
e = math.e

_pm = chr(177)
latitude = -20.352760 # latitude in Velha-ES, Brazil
altitude = 0 # height in Vila Velha-ES, Brazil

# Angle unit. Default is radians
_ang_unit = 'r'


def set_angle_unit(unit = None):
    """ set_angle_unit(unit): set angle unit to degrees (d) or radians (r) """
    global _ang_unit
    if unit == None:
        print '"%s"' % ('degrees' if _ang_unit == 'd' else 'radians')
    elif unit in ('d', 'degrees', 'deg'):
        _ang_unit = 'd'
    elif unit in ('r', 'radians', 'rad'):
        _ang_unit = 'r'
    else:
        _ang_unit = 'd'
        print 'ERROR: Angle unit unknow. Set unit to degrees.'


def is_medida(obj):
    """ is_medida(obj): retorna verdadeiro se o objeto passado é uma medida """
    return hasattr(obj, 'val') and hasattr(obj, 'inc')


def to_medida(obj):
    """ to_medida(obj): transforma o objeto passado para uma medida """
    if is_medida(obj):
        return obj
    else:
        return medida(obj)


def val(obj):
    """ val(obj): retorna o Valor de uma medida """
    if is_medida(obj):
        return obj.val
    return 0


def inc(obj):
    """ inc(obj): retorna a incerteza de uma medida """
    if is_medida(obj):
        return obj.inc
    return 0


class medida():
    """ medida(Valor, Incerteza): medida é uma classe para operações matemáticas
    com medidas Físicas: Valor +- Incerteza """

    def __init__(self, val = 0., inc = 0.):
        if is_medida(val):
            self.val = val.val
            self.inc = val.inc
        else:
            self.val = float(val)
            self.inc = float(inc)


    def __repr__(self):
        if not self.inc:
            return '(%r)' % (self.val)
        else:
            return '(%r %s %r)' % (self.val, _pm, self.inc)


    def __str__(self):
        if not self.inc:
            return '(%r)' % (self.val)
        else:
            return '(%r %s %r)' % (self.val, _pm, self.inc)


    def __neg__(self):
        return Medidas(-self.val, self.inc)


    def __pos__(self):
        return self


    def __add__(self, other):
        other = to_medida(other)
        return medida(self.val + other.val, self.inc + other.inc)


    def __sub__(self, other):
        other = to_medida(other)
        return medida(self.val - other.val, self.inc + other.inc)


    def __rsub__(self, other):
        other = to_medida(other)
        return other - self


    def __mul__(self, other):
        if is_medida(other):
            _val = float(self.val*other.val)
            _inc = abs(_val)*(self.inc/abs(self.val) + other.inc/abs(other.val))
            return medida(_val, _inc)
        else:
            _val = float(self.val*other)
            return medida(_val, abs(other*self.inc))


    __rmul__ = __mul__


    def __div__(self, other):
        if is_medida(other):
            _val = float(self.val/other.val)
            _inc = abs(_val)*(self.inc/abs(self.val) + other.inc/abs(other.val))
        else:
            _val = float(self.val/other)
            _inc = abs(self.inc/other)

        return medida(_val, _inc)


    __truediv__ = __div__


    def __rdiv__(self, other):
        if is_medida(other):
            _val = float(other.val/self.val)
            _inc = abs(_val)*(self.inc/abs(self.val) + other.inc/abs(other.val))
        else:
            _val = float(other/self.val)
            _inc = abs(_val)*self.inc/abs(self.val)

        return medida(_val, _inc)



    __rtruediv__ = __rdiv__


    def __pow__(self, n):
        if is_medida(n):
            _pot = n.val
        else:
            _pot = n
        _val = math.pow(self.val, n)
        _inc = abs(_val)*n*self.inc/abs(self.val)
        return medida(_val, _inc)


    def __rpow__(self, base):
        return pow(self, base)


    def copy(self):
        m = medida(self.val, self.inc)
        return m


measure = medida


# Trunca o valor de uma medida e retorna uma string
def trunc(m):
    """ trunc(m): retorna uma string com a medida truncada """
    if is_medida(m):
        order_inc = order(m.inc)
        order_val = order(m.val)

        # verifica inc*10^(-order_inc) >= 9.5
        inc = 0 # incremento para as condições (order_val > order_inc) e (order_val < order_inc)
        t = m.inc*10**(-order_inc)
        if t >= 9.5:
            inc = 1         # adiciona incremento a ordem de grandeza da incerteza
            order_inc += 1  # o mesmo acima, mas para a condição (order_val == order_inc)

        if order_val > order_inc:
            z = m*10**(-order_val)
            n_order = -order(z.inc) - inc

            if order_val == 0:
                s = '{0} {1} {2}'.format(round(z.val, n_order), _pm, round(z.inc, n_order))
            else:
                s = '({0} {1} {2})E{3}'.format(round(z.val, n_order), _pm, \
                                                         round(z.inc, n_order), order_val)

        elif order_val == order_inc:
            z = m*10**(-order_val)
            if order_inc == 0:
                s = '{0} {1} {2}'.format(int(round(z.val)), _pm, int(round(z.inc)))
            else:
                s = '({0} {1} {2})E{3}'.format(int(round(z.val)), _pm, \
                                                         int(round(z.inc)), order_val)
        else: # order_val < order_inc:
            z = m*10**(-order_inc)
            n_order = -order(z.inc) - inc
            if order_inc == 0:
                s = '{0} {1} {2}'.format(int(round(z.val, n_order)), _pm, \
                                                         int(round(z.inc, n_order)))
            else:
                s = '({0} {1} {2})E{3}'.format(int(round(z.val, n_order)), _pm, \
                                                         int(round(z.inc, n_order)), order_inc)
        return s

    else:
        # não faz nada caso não seja uma Medida
        return m


def order(value):
    """ order(value): Retorna a ordem de grandeza de 'r' """
    val = abs(value)
    count = 0
    if value != 0:
        if val >= 1.:
            step = 1
            ten = .1
            count = 1
        else:
            step = -1
            ten = 10.

        while val < 1 or val >= 10:
            count += step
            val *= ten

    count = count - 1 if count > 0 else count

    return count


def sqrt(m):
    """ sqrt(m): retorna a raiz de uma medida ou real """
    if is_medida(m):
        r = math.sqrt(m.val)
        return medida(r, r*0.5*m.inc/m.val)
    else:
        return math.sqrt(m)


raiz = sqrt


def cos(m):
    """ cos(m): retorna o cosseno de uma medida ou real """
    mm = radians(m) if _ang_unit == 'd' else m

    if is_medida(mm):
        _cos = (math.cos(mm.val + mm.inc) + math.cos(mm.val - mm.inc))/2.
        _dcos = abs(math.cos(mm.val + mm.inc) - math.cos(mm.val - mm.inc))/2.
        return medida(_cos, _dcos)
    else:
        return math.cos(mm)


def cosh(m):
    """ cosh(m): retorna o cosseno hiperbólico de uma medida ou real """
    if is_medida(m):
        _cosh = (math.cosh(m.val+m.inc)+math.cosh(m.val-m.inc))/2.
        _dcosh = abs(math.cosh(m.val+m.inc)-math.cosh(m.val-m.inc))/2.
        return medida(_cosh, _dcosh)
    else:
        return math.cosh(m)


def sin(m):
    """ sin(m): retorna o seno de uma medida ou real """
    mm = radians(m) if _ang_unit == 'd' else m

    if is_medida(mm):
        _sin = (math.sin(mm.val + mm.inc) + math.sin(mm.val - mm.inc))/2.
        _dsin = abs(math.sin(mm.val + mm.inc) - math.sin(mm.val - mm.inc))/2.
        return medida(_sin, _dsin)
    else:
        return math.sin(mm)


def sinh(m):
    """Retorna o seno hiperbólico de uma medida ou real"""
    if is_medida(m):
        _sinh = (math.sinh(m.val+m.inc)+math.sinh(m.val-m.inc))/2.
        _dsinh = abs(math.sinh(m.val+m.inc)-math.sinh(m.val-m.inc))/2.
        return medida(_sinh, _dsinh)
    else:
        return math.sinh(m)


def tan(m):
    """ tan(m): retorna a tangente de uma medida ou real """
    mm = radians(m) if _ang_unit == 'd' else m

    if is_medida(mm):
        _tan = (math.tan(mm.val + mm.inc) + math.tan(mm.val - mm.inc))/2.
        _dtan = abs(math.tan(mm.val + mm.inc) - math.tan(mm.val - mm.inc))/2.
        return medida(_tan, _dtan)
    else:
        return math.tan(mm)


def tanh(m):
    """ tanh(m): retorna a tangente hiperbólica de uma medida ou real """
    if is_medida(m):
        _tanh = (math.tanh(m.val+m.inc)+math.tanh(m.val-m.inc))/2.
        _dtanh = abs(math.tanh(m.val+m.inc)-math.tanh(m.val-m.inc))/2.
        return medida(_tanh, _dtanh)
    else:
        return math.tanh(m)


def log(m, b = e):
    """ log(m,b = e): retorna o logaritomo na base b (e), de uma medida ou real """
    if is_medida(m):
        _log = (math.log(m.val + m.inc, b) + math.log(m.val - m.inc, b))/2.
        _dlog = abs(math.log(m.val + m.inc, b) - math.log(m.val - m.inc, b))/2.
        return medida(_log, _dlog)
    else:
        return math.log(m, b)


def ln(m):
    """ log(m,base = e): retorna o logaritomo natural de uma medida ou real """
    return log(m, e)


def log10(m):
    """ log10(m): retorna o logaritomo base 10 de uma medida ou real """
    if is_medida(m):
        _log10 = (math.log10(m.val+m.inc)+math.log10(m.val-m.inc))/2.
        _dlog10 = abs(math.log10(m.val+m.inc)-math.log10(m.val-m.inc))/2.
        return medida(_log10, _dlog10)
    else:
        return math.log10(m)


def exp(m):
    """ exp(m): retorna a exponecial de uma medida ou real """
    if is_medida(m):
        _exp = (math.exp(m.val+m.inc)+math.exp(m.val-m.inc))/2.
        _dexp = abs(math.exp(m.val+m.inc)-math.exp(m.val-m.inc))/2.
        return medida(_exp, _dexp)
    else:
        return math.exp(m)


def atan(m):
    """ atan(m): retorna o arco-tangente de uma medida ou real """
    if is_medida(m):
        _atan = (math.atan(m.val+m.inc)+math.atan(m.val-m.inc))/2.
        _datan = abs(math.atan(m.val+m.inc)-math.atan(m.val-m.inc))/2.
        if _ang_unit == 'r':
            return medida(_atan, _datan)
        else:
            return medida(degrees(_atan), degrees(_datan))
    else:
        if _ang_unit == 'r':
            return math.atan(m)
        else:
            return math.degrees(math.atan(m))


def asin(m):
    """ asin(m): retorna o arco-seno de uma medida ou real """
    if is_medida(m):
        _asin = (math.asin(m.val+m.inc)+math.asin(m.val-m.inc))/2.
        _dasin = abs(math.asin(m.val+m.inc)-math.asin(m.val-m.inc))/2.
        if _ang_unit == 'r':
            return medida(_asin, _dasin)
        else:
            return medida(degrees(_asin), degrees(_dasin))
    else:
        if _ang_unit == 'r':
            return math.asin(m)
        else:
            return math.degrees(math.asin(m))


asen = asin


def acos(m):
    """ acos(m): retorna o arco-cosseno de uma medida ou real """
    if is_medida(m):
        _acos = (math.acos(m.val+m.inc)+math.acos(m.val-m.inc))/2.
        _dacos = abs(math.acos(m.val+m.inc)-math.acos(m.val-m.inc))/2.
        if _ang_unit == 'r':
            return medida(_acos, _dacos)
        else:
            return medida(degrees(_acos), degrees(_dacos))
    else:
        if _ang_unit == 'r':
            return math.acos(m)
        else:
            return math.degrees(math.acos(m))


def atanh(m):
    """ acosh(m): retorna o arco-cosseno-hiperbólico de m """
    if is_medida(m):
        _atanh = (math.atanh(m.val+m.inc)+math.atanh(m.val-m.inc))/2.
        _datanh = abs(math.atanh(m.val+m.inc)-math.atanh(m.val-m.inc))/2.
        return medida(_acosh, _dacosh)
    else:
        return math.acosh(m)


def asinh(m):
    """ acosh(m): retorna o arco-cosseno-hiperbólico de m """
    if is_medida(m):
        _asinh = (math.asinh(m.val+m.inc)+math.asinh(m.val-m.inc))/2.
        _dasinh = abs(math.asinh(m.val+m.inc)-math.asinh(m.val-m.inc))/2.
        return medida(_acosh, _dacosh)
    else:
        return math.acosh(m)


def acosh(m):
    """ acosh(m): retorna o arco-cosseno-hiperbólico de m """
    if is_medida(m):
        _acosh = (math.acosh(m.val+m.inc)+math.acosh(m.val-m.inc))/2.
        _dacosh = abs(math.acosh(m.val+m.inc)-math.acosh(m.val-m.inc))/2.
        return medida(_acosh, _dacosh)
    else:
        return math.acosh(m)


def radians(m):
    """ radians(m): transforma de graus para radianos uma medida ou real """
    if is_medida(m):
        return medida(math.radians(m.val), math.radians(m.inc))
    else:
        return math.radians(m)


radianos = radians


def degrees(m):
    """ degrees(m): transforma de radianos para graus uma medida ou real """
    if is_medida(m):
        return medida(math.degrees(m.val), math.degrees(m.inc))
    else:
        return math.degrees(m)


graus = degrees


def media(*v):
    """ media(*vetor): retorna uma medida com a média e o desvio médio dos
    valores passados """
    soma = 0.
    for valor in v:
        soma += valor
    media = soma/len(v)

    desv = 0.
    for valor in v:
        desv += abs(valor - media)
    desv /= len(v)

    return medida(media, desv)


def acc_gravity(l = latitude, h = altitude):
    """ acc_gravity(l, h): return gravitational acceleration (g) in the latitude l,
    and altitude h, in m/s^2"""
    g = 9.780327*(1 + 0.0053024*(sin(l))**2-0.0000058*(sin(2*l))**2-h*3.155E-7)
    return g


def medidas_test():
    """ medidas_test(): testa a classe e as funções de Medidas """
    print '\nMódulo medidas.py\n'

    A = medida(3.43, .05)
    B = medida(.046, .002)
    C = medida(66.23, .03)
    D = medida(2.0045, .0005)

    print 'A = ', trunc(A)
    print 'B = ', trunc(B)
    print 'C = ', trunc(C)
    print 'D = ', trunc(D)
    print

    print 'A + D =',
    print trunc(A+D)
    print 'Check = 5.43 %s 0.05\n' % _pm

    print 'A * B =',
    print trunc(A*B)
    print 'Check = 0.158 %s 0.009\n' % _pm

    print 'B**2/C =',
    print trunc(B**2/C)
    print 'Check  = 3.2e-05 %s 3e-06\n' % _pm

    print '2*B**2+4*D =',
    print trunc(2*B**2+4*D)
    print 'Check      = 8.022 %s 0.002\n' % _pm

    print 'C*log(B/D) =',
    print trunc(C*log(B/D))
    print 'Check      = -250 %s 3\n' % _pm

    print 'C*tan(radians(3*C/A**2)) =',
    print trunc(C*tan(radians(3*C/A**2)))
    print 'Check                    = 20.1 %s 0.6\n' % _pm

    print '3*D*sin(radians(2*C)) =',
    print trunc(3*D*sin(radians(2*C)))
    print 'Check                 = 4.436 %s 0.005\n' % _pm

    print 'A + B + C + D =',
    print trunc(A+B+C+D)
    print 'Check         = 71.71 %s 0.08\n' % _pm

    set_angle_unit()
    print '\nNesta versão você pode configurar a unidade padrão para' + \
          ' trabalhar com ângulos, usando a função set_angle_unit()\n'
    print set_angle_unit.__doc__
    print


# constants
u0 = 4E-7*pi
c = 299792458.
e0 = 1/(u0*c**2)
g = medida(acc_gravity(-20.35640, 0.), 1e-3)
ce = 1.602176487E-19
me = 9.10938215E-31
G = 6.67428E-11


if __name__ == '__main__':
    print 'Biblioteca %s' % __lib_name__
    print 'versão %s' % __version__
    print 'Por Rudson Alves'
    print
    print 'Use medidas_test() para ver um exemplo de operação da biblioteca\n'
    print '\nA unidade corrente para ângulos é:'
    set_angle_unit()
    print '\nUse: set_angle_unit(\'u\')\n\nonde u deve ser \'d\' para ' + \
          'graus (degrees), \'r\' para radianos ou sem argumento\n' + \
          'para mostrar a unidade corrente.'
