from operator import itemgetter
import time
import turtle

class MeteoritesEnv:
    def __init__(self, config):
        ax, ay, dt, observable_region_sizes, meteorites_config = itemgetter('ax', 'ay', 'dt', 'observable_region_sizes', 'meteorites')(config)
        self.ax = ax
        self.ay = ay
        self.dt = dt

        r_w, r_h = observable_region_sizes
        llx, urx, lly, ury = (-r_w / 2, r_w / 2, 0, r_h)
        self.observable_region = (llx, lly, urx, ury)

        self.meteorites = { met['id'] : { 'px': met['px'], 'py': met['py'], 'p0x': met['px'], 'p0y': met['py'], 'v0x': met['vx'], 'v0y': met['vy'] }
            for met in meteorites_config }
        self.t = 0

    def meteorite_is_observable(self, mid):
        llx, lly, urx, ury = self.observable_region
        m = self.meteorites[mid]
        return llx <= m['px'] and m['px'] <= urx and lly <= m['py'] and m['py'] <= ury

    def step(self):
        # x(t) = x(0) + v(0) t + a t^2 / 2
        self.t += self.dt
        observable_mets = []
        for mid, m in self.meteorites.items():
            m['px'] = m['p0x'] + m['v0x'] * self.t + self.ax * self.t**2 / 2
            m['py'] = m['p0y'] + m['v0y'] * self.t + self.ay * self.t**2 / 2
            if self.meteorite_is_observable(mid):
                observable_mets.append([mid, m['px'], m['py']])
        return observable_mets


class EnvDisplay:
    def __init__(self, observable_region_sizes, width=800):
        r_w, r_h = observable_region_sizes
        llx, urx, lly, ury = (-r_w / 2, r_w / 2, 0, r_h)
        W_H_ratio = r_w / r_h
        W = width
        H = W / W_H_ratio

        self.screen = turtle.Screen()
        self.screen.setup(width=W, height=H)
        self.screen.setworldcoordinates(llx, lly, urx, ury)
        self.screen.tracer(0)

        self.met_size = 0.4

        self.met_turtles = {}

    def step(self, dt, observable_mets):
        for mt in self.met_turtles.values():
            mt.clear()
            mt.hideturtle()

        for (mid, mx, my) in observable_mets:
            if mid not in self.met_turtles.keys():
                tur = turtle.Turtle()
                tur.hideturtle()
                tur.shape("circle")
                tur.color("#333333")
                tur.shapesize(self.met_size, self.met_size)
                tur.penup()
                self.met_turtles[mid] = tur
            self.met_turtles[mid].setposition(mx, my)
            self.met_turtles[mid].showturtle()

        self.screen.update()
        time.sleep(dt)



def run(config):
    env = MeteoritesEnv(config)
    display = EnvDisplay(config['observable_region_sizes'])

    while True:
        observable_mets = env.step()
        display.step(config['dt'], observable_mets)



if __name__ == '__main__':
    config = {
        'ax': 0.01,
        'ay': -0.03,
        'dt': 0.1,
        'observable_region_sizes': (10, 10),
        'meteorites': [
            {
                'id': 1,
                'px': 0.0,
                'py': 5.0,
                'vx': 0.01,
                'vy': -0.03,
            },
            {
                'id': 2,
                'px': -4.5,
                'py': 9.5,
                'vx': -0.01,
                'vy': -0.02,
            }
        ]
    }

    run(config)
