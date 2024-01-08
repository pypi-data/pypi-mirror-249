use log::debug;
use pyo3::exceptions::PyBaseException;
use pyo3::prelude::*;

use crate::plugin::{
    constants::PluginConstants,
    errors::advance_errors::AdvanceProblem,
    game_state::AdvanceInfo,
    game_state::GameState,
};
use crate::plugin::field::FieldType;
use crate::plugin::ship::Ship;

#[pyclass]
#[derive(PartialEq, Eq, PartialOrd, Clone, Debug, Hash, Copy)]
pub struct Advance {
    /// The number of fields to advance. A negative value means moving backward.
    #[pyo3(get, set)]
    pub distance: i32,
}

#[pymethods]
impl Advance {
    #[new]
    pub fn new(distance: i32) -> Self {
        debug!("New Advance with distance: {}", distance);
        Advance { distance }
    }
    pub fn perform(&self, state: &GameState) -> Result<Ship, PyErr> {
        debug!("Performing advance with distance: {}", self.distance);
        let mut current_ship: Ship = state.current_ship.clone();
        if
            (self.distance < PluginConstants::MIN_SPEED &&
                state.board.get(&current_ship.position).unwrap().field_type !=
                    FieldType::Sandbank) ||
            self.distance > PluginConstants::MAX_SPEED
        {
            debug!("Invalid distance error with distance: {}", self.distance);
            return Err(PyBaseException::new_err(AdvanceProblem::InvalidDistance.message()));
        }
        if self.distance > current_ship.movement {
            debug!(
                "Movement points missing error with distance: {} and movement: {}",
                self.distance,
                current_ship.movement
            );
            return Err(PyBaseException::new_err(AdvanceProblem::MovementPointsMissing.message()));
        }
        let result: AdvanceInfo = state.calculate_advance_info(
            &current_ship.position,
            &(if self.distance < 0 {
                current_ship.direction.opposite()
            } else {
                current_ship.direction
            }),
            current_ship.movement
        );
        if (result.distance() as i32) < self.distance.abs() {
            debug!(
                "Advance problem with available distance: {} and requested distance: {}",
                result.distance(),
                self.distance
            );
            debug!("Advance problem reason: {}", result.problem.message());
            return Err(PyBaseException::new_err(result.problem.message()));
        }
        current_ship.position += current_ship.direction.vector() * self.distance;
        current_ship.movement -= result.cost_until(self.distance as usize);

        debug!("Advance completed and ship status: {:?}", current_ship);
        Ok(current_ship)
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("Advance({})", self.distance))
    }
}

#[cfg(test)]
mod tests {
    use pyo3::prepare_freethreaded_python;
    
    use crate::plugin::board::Board;
    use crate::plugin::coordinate::{ CubeCoordinates, CubeDirection };
    use crate::plugin::field::Field;
    use crate::plugin::game_state::GameState;
    use crate::plugin::segment::Segment;
    use crate::plugin::ship::{ Ship, TeamEnum };

    use super::*;

    #[test]
    fn test_new_advance() {
        let advance: Advance = Advance::new(5);
        assert_eq!(advance.distance, 5);
    }

    fn setup() -> GameState {
        let segment: Vec<Segment> = vec![Segment {
            direction: CubeDirection::Right,
            center: CubeCoordinates::new(0, 0),
            fields: vec![vec![Field::new(FieldType::Water, None); 4]; 5],
        }];
        let board: Board = Board::new(segment, CubeDirection::Right);
        let team_one: &mut Ship = &mut Ship::new(
            CubeCoordinates::new(0, -1),
            TeamEnum::One,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        );
        team_one.speed = 5;
        team_one.movement = 5;
        let team_two: &mut Ship = &mut Ship::new(
            CubeCoordinates::new(-1, 1),
            TeamEnum::Two,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        );
        team_two.speed = 5;
        team_two.movement = 5;
        let game_state: GameState = GameState::new(
            board,
            0,
            team_one.clone(),
            team_two.clone(),
            None
        );
        game_state
    }

    #[test]
    fn test_advance_perform_valid() {
        let advance: Advance = Advance::new(2);
        let state: GameState = setup();

        let result: Result<Ship, PyErr> = advance.perform(&state);

        assert!(result.is_ok());
        let new_ship: Ship = result.unwrap();
        assert_eq!(new_ship.position, CubeCoordinates::new(2, -1));
        assert_eq!(new_ship.movement, 3);
    }

    #[test]
    fn test_advance_perform_invalid_distance() {
        let advance: Advance = Advance::new(-2);
        let state: GameState = setup();

        let result: Result<Ship, PyErr> = advance.perform(&state);

        assert!(result.is_err());
        let error: PyErr = result.unwrap_err();

        prepare_freethreaded_python();
        Python::with_gil(|py| {
            assert_eq!(error.value(py).to_string(), AdvanceProblem::InvalidDistance.message());
        });
    }

    #[test]
    fn test_advance_perform_movement_points_missing() {
        let advance: Advance = Advance::new(6);
        let state: GameState = setup();

        let result: Result<Ship, PyErr> = advance.perform(&state);

        assert!(result.is_err());
        let error: PyErr = result.unwrap_err();

        prepare_freethreaded_python();
        Python::with_gil(|py| {
            assert_eq!(
                error.value(py).to_string(),
                AdvanceProblem::MovementPointsMissing.message()
            );
        });
    }
}
