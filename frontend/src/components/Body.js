import React from 'react';
import About from './About';
import UserInfo from './UserInfo';

/**
 * Component for main page
 * @param {JSON object} searchResult the user information including user_name, repo_number, one_yr_contribution_number,
 * repo_name, repo_description, repo_language.
 * @return {HTML} <UserInfo repos={repos} basics={basics}/> | <About />
 * @example
 * // returns <UserInfo repos={repos} basics={basics}/>
 * Body = ({"user_info": {"username": "Jane", "repo_number": "2",
    "one_yr_contribution_number": "21"}, "repos_info": [{"repo_name": "repo1", "repo_lang": "Python,
    "repo_description": "some description"}, {"repo_name": "repo2", "repo_lang": "C++,
    "repo_description": "some other description"}]})
 * @example
 * // returns <About />
 *      Body = (None)
 */
const Body = ({searchResult}) => {
    if (searchResult){
        const repos = searchResult.repos_info;
        const basics = searchResult.user_info;
        return <UserInfo repos={repos} basics={basics}/>
    }
    else {
        return <About />
    }
};
export default Body;
