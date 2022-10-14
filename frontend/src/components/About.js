import React from 'react';
import logo from '../images/logo.png';

/**
 * Component for landing page.
 * @param {null}
 * @return {HTML}
 * @example
 *      About()
 */
const About = () => {
    return (
        <div id="cent" class="row" background="../images/background.png">
            <>
                <>
                    <>
                        <img src={logo} width="80" alt="Logo"/>
                        <h1>GetHub</h1>
                    </>

                    <h3>
                            Built For  |
                    </h3>
                    <span class="blue-text">
                            Joyful Discovery...We invite you to explore <span class="bold">GitHub</span> repositories by entering GitHub username. Search today!
                    </span>
                </>
            </>
        </div>
    );
};
export default About;
