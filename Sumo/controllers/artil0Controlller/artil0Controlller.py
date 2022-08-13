#RobotName: Artil
from RobotRL import RobotRL
robot = RobotRL()


def noCaer():
    if (robot.getColorPiso() > 90):
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
robot.esperar(1)
previo = 0

while robot.step():
    posicion, flagesp = sensar()
    # print(sen_val)
    #print("Tiempo ",robot.tiempoActual())
    # print(posicion,flagesp)
    error = posicion-50
    abs_error = abs(error)
    #print ("Error     ", error)
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
    velMotorL = -error+po-ew
    velMotorR = error+po+ew
    robot.setVel(velMotorL, velMotorR)
    noCaer()
    actual = robot.tiempoActual()
    if (actual - previo) > 10:
        previo = actual
        robot.setVel(-100, -100)
        robot.esperar(.5)
        robot.setVel(100, 100)
        robot.esperar(.5)
        print("previo")
    # buscar()
    # noCaer()
    # siempre dejar lo mas critico al final, porque ese es el estado en el que quedara si se cumple la
    # condicion de esa llamada
