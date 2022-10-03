import React from 'react';
import Repo from './Repo';

/**
 * Component to display the information for a given username
 * @param {JSON, JSON} repo contains information about repo_name, repo_lang, repo_description; basics contains
 * information about the user including user_name, repo_number and one_yr_contribution_number
 * @return {HTML}
 * @example
 *      UserInfo({repos:{"repo_name": "Repo1", "repo_lang":"JavaScript", "repo_description": "description for repo1"},
 *  basics: {"user_name": "Jane", "repo_numbers: "1", "one_yr_contribution_number": "2"}}
 */
const UserInfo = ({repos, basics}) => {
    const {user_name, repo_number, one_yr_contribution_number} = basics
    return (
        <>
            <h2 class="username">{user_name}</h2>
            <div class="basics">
                <div>
                    <h3 class="nums1">Repository: {repo_number}</h3>
                </div>
                <div>
                    <h3 class="nums2">Last Year Contribution: {one_yr_contribution_number}</h3>
                </div>
            </div>

            <div class="repo">
                <ul>
                    {repos?.map(repo => (
                        <Repo repo={repo} />
                    ))}
                </ul>
            </div>
        </>
    );
};
export default UserInfo;
