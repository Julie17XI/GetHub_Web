import React from 'react';
import axios from 'axios';

/**
 * Component for header on website
 * @param {{state, setState function, function}} state and setState function to set the input in the
 * search box, use the function to send data to root component <App/>
 * @return {HTML}
 * @example
 * // returns HTML that contains logo, search box and a submit button
 *      Header = ({searchInput, setSearchInput,changeSearchResult})
 */
const Header = ({searchInput, setSearchInput,changeSearchResult}) => {
    const handleInput = event => {
        setSearchInput(event.target.value);
    };

    const sendInput = async() => {
        const request = await axios.post(
            `http://127.0.0.1:5000`,
            {
                username: searchInput
            }
        );
        console.log(request);
        changeSearchResult(request.data);
    };

    return (
        <nav class="grey darken-4">
            <div class="nav-wrapper">
                <a href="#" class="brand-logo logo white-text">GetHub</a>
                <ul class="hide-on-med-and-down right">
                    <li>
                        <div class="center row">
                            <div class="col s12 " >
                                <div class="row" id="topbarsearch">
                                    <div class="input-field col s12 indigo.lighten-1">
                                        <input type="text" onChange={handleInput} placeholder="Enter GitHub User..." id="autocomplete-input" class="autocomplete white black-text" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <button onClick={sendInput} class="btn #00838f cyan darken-32" type="submit" name="action">Submit
                        </button>
                    </li>
                </ul>
            </div>
        </nav>
    );
};
export default Header;
