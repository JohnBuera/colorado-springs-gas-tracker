import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.maze import Maze
from backend.optimizer import optimize_stations, normalize_fuel_type
from backend.services import calculate_average_price


def test_average_price_uses_station_list_first():
    assert calculate_average_price([{"prices": {"Regular": 3.0}}, {"prices": {"Regular": 4.0}}], "Regular") == 3.5


def test_api_stats_endpoint():
    response = TestClient(app).get("/prices/stats/regular")
    assert response.status_code == 200
    payload = response.json()
    assert payload["fuel_type"] == "Regular"
    assert payload["average_price"] == pytest.approx((3.45 + 6.75 + 3.75) / 3, abs=.01)


def test_optimizer_respects_fuel_and_returns_route():
    maze = Maze(4, 4)
    maze.generate_maze()
    station = {"name": "Demo Fuel", "cell": (2, 2), "prices": {"MidGrade": 3.12}}
    result = optimize_stations(
        maze, maze.get_cell(0, 0), [station], "mid grade",
        5.0, 15.0, 25.0, 120.0
    )
    assert normalize_fuel_type("Mid Grade") == "midgrade"
    assert result["best"] is not None
    assert result["best"]["price_per_gallon"] == 3.12
    assert result["route"][0] == (0, 0)
    assert result["route"][-1] == (2, 2)


def test_maze_is_connected_and_can_print(capsys):
    maze = Maze(4, 3)
    maze.generate_maze()
    assert maze.is_fully_connected()
    maze.print_maze()
    assert "+" in capsys.readouterr().out
