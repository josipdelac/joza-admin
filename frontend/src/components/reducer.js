const initialState = {
    jwtToken: null, // Postavljanje na null prilikom odjave
  };
  
  const rootReducer = (state = initialState, action) => {
    switch (action.type) {
      case 'LOGOUT':
        return {
          ...state,
          token: null,
        };
      default:
        return state;
    }
  };
  
  export default rootReducer;