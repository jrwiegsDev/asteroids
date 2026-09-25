# Asteroids

The classic arcade game, written in Python with [pygame](https://www.pygame.org/) and compiled to WebAssembly with [pygbag](https://pypi.org/project/pygbag/) so it runs in the browser with nothing to install.

**▶ Play it in your browser:** https://asteroids-1nst.onrender.com

![Asteroids gameplay](https://raw.githubusercontent.com/jrwiegsDev/portfolio-site/main/public/asteroids.png)

## Controls

| Action | Keys |
| --- | --- |
| Rotate | `A` / `D` or `←` / `→` |
| Thrust forward / back | `W` / `S` or `↑` / `↓` |
| Shoot | `Space` |
| Restart after game over | `R` or `Enter` |

## What I built on top of the course project

This started as the guided Asteroids project from [Boot.dev](https://www.boot.dev/)'s backend developer path. From there I added:

- **Score and lives:** smaller asteroids are worth more points. You get 3 lives, with a short blinking invulnerability window after each respawn.
- **Game over and restart** instead of the program exiting on the first hit.
- **Screen wrap** for the ship, arrow-key controls, and an on-screen controls hint.
- **Off-screen cleanup:** shots and asteroids that leave the screen are removed, so the sprite groups don't grow forever.
- **A browser build:** the main loop is `async` and yields to the browser once per frame, which pygbag needs to run the game as WebAssembly.
- **CI/CD:** GitHub Actions checks that every push compiles and builds. Render deploys the static site only after that check passes on `main`.

## Run it locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv run main.py          # desktop window
uv run pygbag .         # browser build, served at http://localhost:8000
```

## How the browser build and deploy work

1. `pygbag --build .` packages the Python source into `build/web/` (an `index.html` plus a small archive of the game code). When the page loads, it downloads a WebAssembly build of CPython and pygame and runs `main.py` in the browser tab. `pygbag.ini` keeps the local `.venv` out of that archive.
2. On every push, [GitHub Actions](.github/workflows/ci.yml) byte-compiles the code and runs the pygbag build, so a broken build fails in CI and never reaches the live site.
3. [Render](render.yaml) hosts `build/web/` as a static site and rebuilds it automatically once CI passes on `main` (`autoDeployTrigger: checksPass`).

## Roadmap

- On-screen touch controls so it's playable on phones
- Sound effects
- High score board
