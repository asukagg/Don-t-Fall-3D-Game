# Don-t-Fall-3D-Game
CSE423 Project

 “Don’t Fall”

1. Shrinking Arena: The game starts with a 5x5 grid of floating platforms (cubes), and every 5 seconds, a random platform turns red for 1 second before disappearing, forcing the player to keep moving or risk falling and ending the game.
2. Player Movement: The player, a character with a cube body and sphere head, moves using WASD keys and jumps with the spacebar to navigate between platforms, with the game ending if they fall off (X/Y exceeds platform bounds or Z drops below 0).
3. Scoring System: A timer tracks survival time in seconds, displayed on the screen, while catching a special spark which randomly appears on the tile grants 10 points each, with the total score being spark catching bonus (10 per one spark).
4. Laser Beams: Thin cylinders act as laser beams that sweep across the arena, turning on for 4 seconds and off for 10 seconds, knocking the player off if touched.
5. Rising Spikes: Spikes randomly rise from platforms and retract after a few seconds if a player is on the platform when spikes appear his earned score resets.
6. Random Portal Spawn: A portal spawns on a platform glowing with cycling colors to attract the player’s attention.
7. Teleport to Difficult Arena: Entering the portal teleports the player to a harder 4x4 grid arena where the difficulty increases as the player has less grids to move to. There will also be a portal in the 4x4 arena to come back to the 5x5 arena again.
8. Visual Effects: Platforms go red before disappearing to warn the player that the grid is going to fall, lasers glow with cycling colors and spikes spawn to reset the score.
9. Background Elements: A large light blue sphere acts as a skybox around the arena
