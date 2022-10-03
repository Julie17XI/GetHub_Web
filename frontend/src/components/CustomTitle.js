import {useEffect, useState} from "react";

/**
 * Component for webpage tag title
 * @param {string} title a title for webpage tag
 * @return {useState object} 
 * @example
 *      CustomTitle("GetHub")
 */
const CustomTitle = (title) => {
    const [customTitle, setCustomTitle] = useState(title);
    useEffect(() => {
        document.title = customTitle;
    }, [customTitle]);

    return [customTitle, setCustomTitle];
}

export default CustomTitle;
