from pygame.mixer import Sound


class SoundWrapper:
    sound: Sound
    is_playing: bool
    interruptable: bool
    volume: float

    def __init__(self,
                 path: str,
                 interruptable: bool = False,
                 volume: float = 1):
        self.volume = volume
        if path == None:
            self.sound = None
        else:
            self.sound = Sound(path)
            self.sound.set_volume(volume)
        self.interruptable = interruptable
        self.is_playing = False

    def play(self, loops: int):
        if not self.sound or (self.is_playing and not self.interruptable):
            return
        self.sound.play(loops)
        self.is_playing = True

    def stop(self):
        if not self.sound:
            return
        self.sound.stop()
        self.is_playing = False

    def set_volume(self, volume: float):
        if not self.sound:
            return
        self.sound.set_volume(volume)
