import React from 'react';

/**
 * Component to display the information of one repository
 * @param {JSON} repo contains information about repo_name, repo_lang, repo_description
 * @return {HTML}
 * @example
 *      Repo({"repo_name": "Repo1", "repo_lang":"JavaScript", "repo_description": ""});
 */
const Repo = ({repo}) => {
    const {repo_name, repo_lang, repo_description} = repo
    return (
        <div class="card repocard">
            <div class="card">
                <div class="card-content reponame">
                <p>{repo_name}</p>
                </div>
                <div class="card-content repotext">
                <p>{repo_description}</p>
                </div>
                <div class="card-action repolang">
                <p>{repo_lang}</p>
                </div>
            </div>
        </div>
    );
};
export default Repo;
