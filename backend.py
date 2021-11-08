class Tile():
    def __init__(self):
        super().__init__()
        # 변하지 않는 초깃값 list()를 사용하여
        # Tile  
        self.black_tile_solid = list(range(0, 24, 2))
        self.white_tile_solid = list(range(1, 24, 2))

        # Player
        self.human_tile_solid = []
        self.AI_tile_solid = []

        self.init_Tile()

    # Tile을 처리하는데 필요한 값을 초기화
    def init_Tile(self): 
        self.black_tile = list(self.black_tile_solid)
        self.white_tile = list(self.white_tile_solid)

        self.human_tile = list(self.human_tile_solid)
        self.AI_tile = list(self.AI_tile_solid)
        
        # 처음 타일 4개 뽑기
        self.pick_random(2, 'B', 'human')
        self.pick_random(2, 'W', 'human')
        self.pick_random(2, 'B', 'AI')
        self.pick_random(2, 'W', 'AI')

    def set_player(self, player_s : str):
        return self.human_tile if player_s.upper() == "HUMAN" else self.AI_tile if player_s.upper() == "AI" else None

    def pick_random(self, N : int, tiles_pick : str, player : str):
        import random

        player = self.set_player(player)
        self.tiles_will_pick = self.black_tile if tiles_pick.upper() == "B" else self.white_tile if tiles_pick.upper() == "W" else None
        if len(tiles_pick) == 0:
            raise Exception("No tiles to pick")

        for _ in range(N):
            random.shuffle(self.tiles_will_pick)
            tile_picked = self.tiles_will_pick[random.randrange(0, len(self.tiles_will_pick))]

            # 현재 상황 정리
            self.tiles_will_pick.remove(tile_picked)
            player.append(tile_picked)
        
        self.last_tile_picked = tile_picked # 반복문이 끝난 후 마지막으로 바뀐 값이 마지막 뽑은 타일이므로

    def order(self, player : str):
        player = sorted(self.set_player(player))

        for idx in range(0, len(player)):
            if player[idx] % 2 == 0: # black
                player[idx] = '{}B'.format(player[idx] // 2)
            else: # white
                player[idx] = '{}W'.format(player[idx] // 2)

        return player
