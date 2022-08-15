#RobotName: Artil
from simple_pid import PID
from RobotRL import RobotRL
robot = RobotRL()


def montado():
    s_piso = robot.getColorPiso()
    # print(s_piso)
    if (s_piso > 77 and s_piso < 86):
        print("retro")
        robot.setVel(100, -100)
        robot.esperar(0.5)


previo = 0


def timecheck():
    global previo
    actual = robot.tiempoActual()
    if (actual - previo) > 10:
        previo = actual
        robot.setVel(-100, 100)
        robot.esperar(.5)
        robot.setVel(100, 100)
        robot.esperar(.5)
        # print("previo")


def noCaer():
    if (robot.getColorPiso() > 90):
        robot.setVel(100, 100)
        robot.esperar(0.5)
        robot.setVel(-100, -100)
        robot.esperar(1)
        robot.setVel(-100, 100)
        robot.esperar(0.5)


sensor = [0, 0]
sen_val = [0, 0]
escapo = True


def sensar():
    sensor[0] = robot.getDI()
    sensor[1] = robot.getDD()
    global escapo
    mass = 0
    torque = 0
    for i in range(2):
        mass += sensor[i]
        torque += sensor[i]*i*100
    centroid = torque/mass

    if centroid != 50:
        escapo = True if centroid < 50 else False
    return (centroid, escapo)


# robot.setVel(50,-50)
# robot.esperar(1)


kp = 1
ki = 0.01
kd = 0.005
pid = PID(kp, ki, kd, 50, 0.01, (-50, 50), True, False, None)

while robot.step():
    # montado()
    posicion, flagesp = sensar()
    print(posicion, flagesp)

    out = pid(posicion)
    # print(out)

    error = posicion-50
    abs_error = abs(error)
    print("Error     ", error)
    if robot.getDI() == 100 and robot.getDD() == 100:
        ew = -30 if flagesp else 30
        po = 20
    elif abs_error < 5:
        ew = 0
        # error=0
        po = 80
        robot.setVel(po, po)
        robot.esperar(0.1)
        # print("Ataque")
    else:
        ew = 0
        po = 0
    vl = 50
    robot.setVel(out+vl-ew, -out+vl+ew)
    # velMotorL = -error  #+po-ew
    # velMotorR = error   #+po+ew
    #robot.setVel(velMotorL, velMotorR)
    # noCaer()
    # buscar()
    timecheck()
    noCaer()
    # siempre dejar lo mas critico al final, porque ese es el estado en el que quedara si se cumple la
    # condicion de esa llamada
