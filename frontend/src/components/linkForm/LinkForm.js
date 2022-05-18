import React from 'react';
import {copyToClipboard, goToAddLocationPage} from "../../utils";

export const LinkForm = props => {
    return (
        <form className="form">
            <p>{props.message}</p>
            <div className="location-url">
                <div className="url-text">
                    <span>{props.textToCopy}</span>
                    <div id="copied" className="copied-link">link has been copied!</div>
                </div>
                <div className="copy-location">
                    <button onClick={(event) => copyToClipboard(event, props.textToCopy, "copied")}>
                        <div className="icon-holder">
                            <i className="icon-copy"/>
                        </div>
                        <span>copy to <br/>clipboard</span>
                    </button>
                </div>
            </div>
            <p>Share this URL with a friend to find places to meet in the middle.</p>
            <button onClick={(event) => {
                goToAddLocationPage(event, window.location.pathname)
            }} type="submit" className="btn-primary">Add another Location <i className="icon-right-2"/></button>
        </form>
    );
};
