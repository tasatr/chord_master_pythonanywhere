import React from 'react';

class Searchbar extends React.Component {
    handleChange = (event) => {
        console.log('inside handleChange');
        this.setState({
            term: event.target.value
        });

    };
    handleSubmit = event => {
        console.log('olen siin');
        console.log(this.state.term);
        event.preventDefault();
        this.props.handleFormSubmit(this.state.term);
    }

    render() {

        return (
            <>
            <div className='search-bar ui segment'>
                <form onSubmit={this.handleSubmit} className='ui form'>
                    <div className='field'>
                        <label htmlFor="video-search">YouTube Video Search</label>
                        <input onChange={this.handleChange} name='video-search' type="text" placeholder="Search.."/>
                    </div>
                </form>
            </div>
            </>
        )
    }
}
export default Searchbar;
