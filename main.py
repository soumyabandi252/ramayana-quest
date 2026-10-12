"""Ramayana Quest - 5 mini-game levels based on the epic. Web + desktop (pygame)."""
import asyncio, pygame, random, sys
pygame.init()
W, H = 900, 560
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ramayana Quest")
clock = pygame.time.Clock()
F = pygame.font.SysFont("arial", 22)
FB = pygame.font.SysFont("arial", 40, bold=True)

LEVELS = [
 ("Chapter 1: Sita Swayamvara", "Bend Shiva's bow. Press SPACE when the power bar is in the green zone."),
 ("Chapter 2: Dandaka Forest", "Defend Sita! LEFT/RIGHT move Rama, SPACE shoots arrows at Khar's demons. Stop 15."),
 ("Chapter 3: Hanuman Leaps to Lanka", "UP/DOWN to fly over the ocean. Dodge sea-monsters, grab flowers. Collect 8."),
 ("Chapter 4: Ram Setu", "LEFT/RIGHT to catch stones marked RAMA. Build 12 to finish the bridge. Don't miss 5."),
 ("Chapter 5: Rama vs Ravana", "LEFT/RIGHT aim, SPACE shoot. Hit each of the 10 heads, then hold SPACE to charge the Brahmastra."),
]

def txt(s, x, y, font=F, c=(255,255,255), center=False):
    img = font.render(s, True, c)
    r = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
    screen.blit(img, r)

def wrap(s, x, y, width=60):
    line = ""
    for w in s.split():
        if len(line + w) > width:
            txt(line, x, y); y += 28; line = ""
        line += w + " "
    txt(line, x, y)

class Level:
    done = False; failed = False
    def event(self, e): pass
    def update(self): pass
    def draw(self): pass

class Bow(Level):
    def __init__(self):
        self.p = 0; self.d = 1; self.fired = False; self.t = 0; self.tries = 3
    def event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and not self.fired:
            if 70 <= self.p <= 88:
                self.fired = True; self.t = 60
            else:
                self.tries -= 1
                if self.tries == 0: self.failed = True
    def update(self):
        if self.fired:
            self.t -= 1
            if self.t <= 0: self.done = True
            return
        self.p += self.d * (1.6 + (3 - self.tries) * 0.8)
        if self.p >= 100 or self.p <= 0: self.d *= -1
    def draw(self):
        screen.fill((60, 40, 20))
        pygame.draw.rect(screen, (30,30,30), (150, 300, 600, 40))
        pygame.draw.rect(screen, (40,180,60), (150+420, 300, 108, 40))
        pygame.draw.rect(screen, (255,200,0), (150+self.p*6-4, 290, 8, 60))
        txt(f"Tries left: {self.tries}", 20, 20)
        if self.fired: txt("CRACK! The bow breaks. Sita garlands Rama!", W//2, 200, FB, (255,220,120), True)
        else: txt("Rama lifts the mighty bow...", W//2, 200, FB, (255,255,255), True)

class Forest(Level):
    def __init__(self):
        self.x = W//2; self.arrows = []; self.en = []; self.kills = 0; self.hp = 5; self.cd = 0; self.sp = 0
    def update(self):
        k = pygame.key.get_pressed()
        self.x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 6
        self.x = max(30, min(W-30, self.x))
        self.cd -= 1
        if k[pygame.K_SPACE] and self.cd <= 0:
            self.arrows.append([self.x, H-80]); self.cd = 15
        self.sp += 1
        if self.sp > 35: self.en.append([random.randint(30, W-30), 0]); self.sp = 0
        for a in self.arrows: a[1] -= 10
        for e in self.en: e[1] += 3
        for a in self.arrows[:]:
            for e in self.en[:]:
                if abs(a[0]-e[0]) < 25 and abs(a[1]-e[1]) < 25:
                    self.arrows.remove(a); self.en.remove(e); self.kills += 1; break
        for e in self.en[:]:
            if e[1] > H-50: self.en.remove(e); self.hp -= 1
        self.arrows = [a for a in self.arrows if a[1] > 0]
        if self.kills >= 15: self.done = True
        if self.hp <= 0: self.failed = True
    def draw(self):
        screen.fill((20, 70, 30))
        pygame.draw.rect(screen, (60,120,255), (self.x-15, H-60, 30, 50))
        txt("Rama", self.x, H-75, F, (255,255,255), True)
        for a in self.arrows: pygame.draw.rect(screen, (255,255,0), (a[0]-2, a[1], 4, 18))
        for e in self.en: pygame.draw.circle(screen, (200,30,30), e, 20)
        txt(f"Demons slain: {self.kills}/15   Sita's safety: {self.hp}", 20, 20)

class Hanuman(Level):
    def __init__(self):
        self.y = H//2; self.obs = []; self.fl = []; self.got = 0; self.hp = 3; self.sp = 0; self.fs = 0
    def update(self):
        k = pygame.key.get_pressed()
        self.y += (k[pygame.K_DOWN] - k[pygame.K_UP]) * 6
        self.y = max(20, min(H-20, self.y))
        self.sp += 1; self.fs += 1
        if self.sp > 40: self.obs.append([W, random.randint(30, H-30)]); self.sp = 0
        if self.fs > 70: self.fl.append([W, random.randint(30, H-30)]); self.fs = 0
        for o in self.obs: o[0] -= 5
        for f in self.fl: f[0] -= 4
        for o in self.obs[:]:
            if abs(o[0]-100) < 30 and abs(o[1]-self.y) < 35: self.obs.remove(o); self.hp -= 1
        for f in self.fl[:]:
            if abs(f[0]-100) < 30 and abs(f[1]-self.y) < 30: self.fl.remove(f); self.got += 1
        self.obs = [o for o in self.obs if o[0] > -50]; self.fl = [f for f in self.fl if f[0] > -50]
        if self.got >= 8: self.done = True
        if self.hp <= 0: self.failed = True
    def draw(self):
        screen.fill((20, 60, 140))
        pygame.draw.rect(screen, (10, 30, 90), (0, H-60, W, 60))
        pygame.draw.circle(screen, (230,140,40), (100, self.y), 22)
        txt("Hanuman", 100, self.y-38, F, (255,255,255), True)
        for o in self.obs: pygame.draw.circle(screen, (30,120,80), o, 24)
        for f in self.fl: pygame.draw.circle(screen, (255,120,200), f, 12)
        txt(f"Flowers: {self.got}/8   Strength: {self.hp}", 20, 20)

class Setu(Level):
    def __init__(self):
        self.x = W//2; self.st = []; self.n = 0; self.miss = 0; self.sp = 0
    def update(self):
        k = pygame.key.get_pressed()
        self.x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 8
        self.x = max(50, min(W-50, self.x))
        self.sp += 1
        if self.sp > 45: self.st.append([random.randint(30, W-30), 0]); self.sp = 0
        for s in self.st[:]:
            s[1] += 4
            if s[1] > H-60 and abs(s[0]-self.x) < 55: self.st.remove(s); self.n += 1
            elif s[1] > H: self.st.remove(s); self.miss += 1
        if self.n >= 12: self.done = True
        if self.miss >= 5: self.failed = True
    def draw(self):
        screen.fill((30, 90, 160))
        pygame.draw.rect(screen, (190, 150, 90), (0, H-20, self.n*W//12, 20))
        pygame.draw.rect(screen, (240,240,240), (self.x-50, H-60, 100, 20))
        for s in self.st:
            pygame.draw.rect(screen, (130,130,130), (s[0]-20, s[1], 40, 30)); txt("RAMA", s[0], s[1]+15, F, (255,255,255), True)
        txt(f"Stones placed: {self.n}/12   Missed: {self.miss}/5", 20, 20)

class Ravana(Level):
    def __init__(self):
        self.x = W//2; self.arrows = []; self.heads = [True]*10; self.cd = 0; self.charge = 0
        self.hp = 5; self.fire = []; self.fs = 0; self.final = False; self.flash = 0
    def hx(self, i): return 120 + i*72
    def update(self):
        k = pygame.key.get_pressed()
        self.x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 6
        self.x = max(30, min(W-30, self.x))
        self.cd -= 1
        if any(self.heads):
            if k[pygame.K_SPACE] and self.cd <= 0: self.arrows.append([self.x, H-80]); self.cd = 18
            self.fs += 1
            if self.fs > 50:
                self.fire.append([self.hx(random.randrange(10)), 110]); self.fs = 0
        elif not self.final:
            if k[pygame.K_SPACE]: self.charge += 1
            else: self.charge = max(0, self.charge - 2)
            if self.charge >= 120: self.flash = 40; self.final = True
        for a in self.arrows: a[1] -= 11
        for f in self.fire: f[1] += 4
        for a in self.arrows[:]:
            for i in range(10):
                if self.heads[i] and abs(a[0]-self.hx(i)) < 28 and a[1] < 130:
                    self.heads[i] = False; self.arrows.remove(a); break
        for f in self.fire[:]:
            if f[1] > H-70 and abs(f[0]-self.x) < 30: self.fire.remove(f); self.hp -= 1
            elif f[1] > H: self.fire.remove(f)
        self.arrows = [a for a in self.arrows if a[1] > 0]
        if self.final:
            self.flash -= 1
            if self.flash <= 0: self.done = True
        elif self.hp <= 0: self.failed = True
    def draw(self):
        screen.fill((255, 230, 150) if self.final else (70, 10, 10))
        for i in range(10):
            if self.heads[i]: pygame.draw.circle(screen, (90,20,120), (self.hx(i), 80), 28)
        pygame.draw.rect(screen, (120,0,0), (70, 105, 760, 25))
        pygame.draw.rect(screen, (60,120,255), (self.x-15, H-60, 30, 50))
        for a in self.arrows: pygame.draw.rect(screen, (255,255,0), (a[0]-2, a[1], 4, 18))
        for f in self.fire: pygame.draw.circle(screen, (255,120,0), f, 10)
        txt(f"Heads left: {sum(self.heads)}   Rama's life: {self.hp}", 20, 20, F, (255,255,255) if not self.final else (0,0,0))
        if not any(self.heads) and not self.final:
            pygame.draw.rect(screen, (50,50,50), (250, 480, 400, 20))
            pygame.draw.rect(screen, (255,200,0), (250, 480, min(400, self.charge*400//120), 20))
            txt("HOLD SPACE: charge the Brahmastra!", W//2, 450, F, (255,255,255), True)

CLASSES = [Bow, Forest, Hanuman, Setu, Ravana]
ENDING = "Ravana falls. Sita is freed. Rama, Sita and Lakshmana return to Ayodhya in the Pushpaka Vimana, and Rama is crowned king. Jai Shri Ram!"

async def main():
    idx, state, lvl = 0, "intro", None
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); return
            if state == "play": lvl.event(e)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if state in ("intro", "fail"): lvl = CLASSES[idx](); state = "play"
                elif state == "win":
                    idx += 1
                    state = "end" if idx >= len(CLASSES) else "intro"
                elif state == "end": idx = 0; state = "intro"
        if state == "play":
            lvl.update()
            if lvl.done: state = "win"
            elif lvl.failed: state = "fail"
        if state == "play": lvl.draw()
        else:
            screen.fill((25, 15, 40))
            if state == "intro":
                txt(LEVELS[idx][0], W//2, 150, FB, (255,200,80), True); wrap(LEVELS[idx][1], 100, 250)
                txt("Press ENTER to start", W//2, 450, F, (200,200,200), True)
            elif state == "fail":
                txt("Defeated... Try again!", W//2, 220, FB, (255,90,90), True); txt("Press ENTER to retry", W//2, 300, F, (200,200,200), True)
            elif state == "win":
                txt("Chapter complete!", W//2, 220, FB, (120,255,120), True); txt("Press ENTER to continue", W//2, 300, F, (200,200,200), True)
            else:
                txt("VICTORY!", W//2, 150, FB, (255,200,80), True); wrap(ENDING, 100, 250); txt("ENTER to play again", W//2, 450, F, (200,200,200), True)
        pygame.display.flip(); clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
