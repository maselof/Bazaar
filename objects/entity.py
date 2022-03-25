import game_logic
from pygame.math import Vector2
from item import *
from weapon import *
import game_cycle
from inventory import GameContainer
from inventory import ILootable
from spectrum import Spectrum


class AI:
    duration: int
    delay: int
    counter: int
    finished: bool

    movement_area: [Vector2]
    movement_point: Vector2
    agro_radius: int
    is_enemy: bool
    is_attacking: bool

    def __init__(self):
        self.duration = 0
        self.delay = 0
        self.counter = 0
        self.finished = True

        self.movement_area = None
        self.movement_point = None
        self.agro_radius = 0
        self.is_enemy = False
        self.is_attacking = False


class Stats:
    vitality: int
    max_hp: int
    hp: int

    endurance: int
    max_stamina: int
    stamina: int

    intellect: int
    max_mana: int
    mana: int

    strength: int
    dexterity: int

    max_exp: int
    exp: int
    lvl: int
    skill_points: int

    attack_speed: float
    movement_speed: float
    damage: float
    dps: float

    def __init__(self,
                 max_hp: int = 100, max_stamina: int = 100, max_mana: int = 100, max_exp: int = 100, exp: int = 0, lvl: int = 0):
        self.vitality = 10
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.endurance = 10
        self.max_stamina = max_stamina
        self.stamina = self.max_stamina
        self.intellect = 10
        self.max_mana = max_mana
        self.mana = self.max_mana
        self.strength = 10
        self.dexterity = 10
        self.max_exp = max_exp
        self.exp = exp
        self.lvl = lvl
        self.skill_points = 0
        self.attack_speed = 1
        self.movement_speed = 0
        self.damage = 10
        self.dps = 10


class Entity(GameObject, ILootable):
    direction_vector: Vector2
    left_flip: bool
    inventory: GameContainer

    stats: Stats

    is_dead: bool

    weapon: Weapon

    attack_rects: [pygame.Rect]
    c_attack_rects: int

    effects: {str: Effect}

    ai: AI
    enable_random_actions: bool

    spectra: {str: Spectrum}
    current_spectrum: Spectrum

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 collision_rect_offset: pygame.Vector2 = Vector2(0, 0),
                 scaling: float = 1,
                 stats: Stats = Stats()
                 ):
        self.weapon = game_logic.get_item('fists')
        super().__init__(name, animations_path, size, collision_rect_offset, True, scaling)

        self.direction_vector = Vector2(0, 0)
        self.left_flip = False
        self.direction = Direction.LEFT

        self.stats = stats
        self.is_dead = False



        self.attack_rects = []
        self.c_attack_rects = 5

        self.inventory = GameContainer()
        self.effects = {}

        self.enable_random_actions = True
        self.ai = AI()
        self.ai.is_enemy = True
        self.ai.agro_radius = game_logic.enemy_agro_radius

        self.spectra = {'get_damage': Spectrum(Vector2(self.collision_rect.size),
                                               Vector2(self.collision_rect.x, self.collision_rect.y),
                                               pygame.Color(255, 255, 255), 20, 250)}
        self.current_spectrum = self.spectra.get('get_damage')

        self.stats = self.get_updated_stats(self.stats)
        self.refresh()
        self.scale_sounds(0)

    def animations_init(self):
        path = 'res/animations/entities/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle', True)),
                        'walking': Action(self.action_walking, Animation(path, 'walking', True, True, game_logic.g_entity_walking_anim_speed)),
                        'attacking': Action(self.action_attacking, Animation(path, 'attacking', True, False, game_logic.g_entity_attacking_anim_speed))}
        self.current_action = self.actions['idle']

    def sounds_init(self):
        self.sounds = {'Steps': SoundWrapper('res/sounds/entities/steps.mp3', False, 0.2)}

    def scale_sounds(self, scaling: float):
        super().scale_sounds(scaling)
        if self.weapon:
            self.weapon.scale_sounds(scaling)

    def stop_sounds(self):
        for sound in self.sounds.values():
            sound.stop()

    def set_position(self, point: pygame.Vector2):
        super().set_position(point)
        self.weapon.set_position(point)
        self.current_spectrum.surface.set_position(Vector2(self.collision_rect.x, self.collision_rect.y))

    def move(self, vector: pygame.Vector2):
        super().move(vector)
        self.weapon.move(vector)
        self.current_spectrum.surface.move(vector)

    def action_idle(self, args: [object]):
        super().action_idle(args)
        self.direction_vector = Direction.STAND.value
        if self.sounds:
            self.sounds.get('Steps').stop()

    def action_walking(self, args: [object]):
        dir_v = game_cycle.game_data.game_map.check_collisions(self, args[0])
        self.direction_vector = dir_v
        new_pos = self.get_position() + self.direction_vector * self.stats.movement_speed
        self.set_position(new_pos)
        if self.sounds:
            self.sounds.get('Steps').play(-1)

    def build_attack_rects(self):
        self.attack_rects.clear()
        height = self.weapon.attack_range // self.c_attack_rects
        for i in range(self.c_attack_rects):
            width = height * (self.c_attack_rects - (i + 1)) * 2
            if is_horizontal(self.direction):
                w = height
                h = width
                pos_x = self.collision_rect.centerx + self.direction.value.x * w * (i + 1 * (self.direction == Direction.LEFT))
                pos_y = self.collision_rect.centery - h // 2
                self.attack_rects.append(pygame.Rect(pos_x, pos_y, w, h))
            else:
                w = width
                h = height
                pos_x = self.collision_rect.centerx - w // 2
                pos_y = self.collision_rect.centery + self.direction.value.y * h * (i + 1 * (self.direction == Direction.UP))
                self.attack_rects.append(pygame.Rect(pos_x, pos_y, w, h))

    def action_attacking(self, args: [object]):
        self.direction_vector = Direction.STAND.value
        if not self.current_action.animation.finished:
            return
        collided = game_cycle.game_data.game_map.get_collided_visible_objects(self, self.attack_rects)
        for go in collided:
            if isinstance(go, Entity):
                self.weapon.sounds.get('Damage').play(0)
                go.get_damage(int(self.stats.damage))
                for effect in self.weapon.attack_effects:
                    effect.start()
                    go.effects.update({effect.name: effect})
        if self.sounds:
            self.sounds.get('Steps').stop()
            self.weapon.sounds.get('Slash').play(0)

    def get_damage(self, damage: int):
        self.stats.hp = max(self.stats.hp - damage, 0)
        self.current_spectrum = self.spectra.get('get_damage')
        self.current_spectrum.start()

    def die(self):
        self.is_dead = True

    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.update_stats()
        self.weapon.actions.get('walking').animation.speed = self.actions.get('walking').animation.speed
        self.weapon.actions.get('attacking').animation.speed = self.actions.get('attacking').animation.speed

    def update_effects(self):
        finished = []
        for effect in self.effects.values():
            effect.update(self)
            if effect.finished:
                finished.append(effect)
        for effect in finished:
            del self.effects[effect.name]

    def do_random_movement(self):
        if self.ai.finished:
            self.ai.finished = False

            if self.ai.movement_area:
                self.ai.movement_point = Vector2(random.randint(int(self.ai.movement_area[0].x), int(self.ai.movement_area[1].x)),
                                                 random.randint(int(self.ai.movement_area[0].y), int(self.ai.movement_area[1].y)))
            else:
                self.ai.movement_point = Vector2(random.randint(-1 * game_logic.entity_movement_area_size.x // 2, 1 * game_logic.entity_movement_area_size.x // 2),
                                                 random.randint(-1 * game_logic.entity_movement_area_size.y // 2, 1 * game_logic.entity_movement_area_size.y // 2)) + self.get_position()

            self.ai.duration = random.randint(60, 300)
            self.ai.delay = random.randint(60, 300)

        elif self.ai.duration != 0:
            self.ai.counter += 1
            if self.ai.counter >= self.ai.duration:
                self.ai.counter = 0
                self.ai.duration = 0

            pos_dif = self.ai.movement_point - self.get_position()
            if abs(pos_dif.x) < 6 and abs(pos_dif.y) < 6:
                self.ai.duration = 0
                return

            direction_vector = pos_dif / max(abs(pos_dif.x), abs(pos_dif.y))

            if abs(direction_vector.x) > abs(direction_vector.y):
                self.direction = Direction.RIGHT if direction_vector.x > 0 else Direction.LEFT
            else:
                self.direction = Direction.DOWN if direction_vector.y > 0 else Direction.UP

            self.set_action('walking', direction_vector)

        else:
            self.set_action('idle', None)
            self.ai.counter += 1
            if self.ai.counter >= self.ai.delay:
                self.ai.finished = True

    def attack_entity(self, entity, distance: int):
        if distance > self.weapon.attack_range:
            pos_dif = entity.get_center() - self.get_center()
            direction_vector = pos_dif / max(abs(pos_dif.x), abs(pos_dif.y))
            if abs(direction_vector.x) > abs(direction_vector.y):
                self.direction = Direction.RIGHT if direction_vector.x > 0 else Direction.LEFT
            else:
                self.direction = Direction.DOWN if direction_vector.y > 0 else Direction.UP
            self.set_action('walking', direction_vector)
        else:
            self.set_action('attacking', None)

    def do_ai(self):
        object, distance = game_cycle.game_data.game_map.get_nearest_object(self)
        if isinstance(object, Entity) and self.ai.is_enemy != object.ai.is_enemy and distance <= self.ai.agro_radius:
            self.attack_entity(object, distance)
        else:
            self.do_random_movement()

    def get_updated_stats(self, stats: Stats):
        new_stats = Stats()
        new_stats.max_hp = stats.vitality * 10
        new_stats.max_stamina = stats.endurance * 10
        new_stats.max_mana = stats.intellect * 10
        new_stats.damage = self.weapon.damage * stats.strength / 10
        new_stats.attack_speed = stats.dexterity / 10 * self.weapon.attack_speed_modifier
        new_stats.dps = round(new_stats.damage * new_stats.attack_speed, 1)
        new_stats.movement_speed = int(stats.dexterity / 10 * game_logic.hero_base_speed)
        new_stats.hp = stats.hp
        new_stats.stamina = stats.stamina
        new_stats.mana = stats.mana
        new_stats.strength = stats.strength
        new_stats.dexterity = stats.dexterity
        new_stats.vitality = stats.vitality
        new_stats.endurance = stats.endurance
        new_stats.intellect = stats.intellect
        new_stats.exp = stats.exp
        new_stats.lvl = stats.lvl
        new_stats.max_exp = stats.max_exp
        new_stats.skill_points = stats.skill_points
        return new_stats

    def update_stats(self):
        self.stats = self.get_updated_stats(self.stats)
        self.actions.get('walking').animation.speed = game_logic.g_entity_walking_anim_speed * self.stats.movement_speed / game_logic.hero_base_speed
        self.actions.get('attacking').animation.speed = game_logic.g_entity_attacking_anim_speed * self.stats.attack_speed

    def refresh(self):
        self.stats.hp = self.stats.max_hp
        self.stats.stamina = self.stats.max_stamina
        self.stats.mana = self.stats.max_mana

    def update(self):
        super().update()

        if self.enable_random_actions:
            self.do_ai()

        self.weapon.set_position(self.get_position())
        self.weapon.direction = self.direction
        self.weapon.set_action(self.current_action.animation.name, self.current_action.args)
        self.weapon.update()
        self.build_attack_rects()
        self.inventory.update()
        self.update_effects()

        if self.current_spectrum:
            self.current_spectrum.update()

        if self.stats.hp == 0:
            self.die()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.weapon.draw(screen)

        if self.current_spectrum and not self.current_spectrum.finished:
            self.current_spectrum.draw(screen)

        # pygame.draw.circle(screen, (0, 255, 0), self.collision_rect.center, self.ai.agro_radius)

        # if self.ai.movement_area:
        #     size = self.ai.movement_area[1] - self.ai.movement_area[0]
        #     pygame.draw.rect(screen, pygame.Color(0, 255, 0), Rect(self.ai.movement_area[0].x, self.ai.movement_area[0].y, size.x, size.y))
