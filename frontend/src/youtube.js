import axios from 'axios';
//import axios, * as others from 'axios';
const KEY = 'AIzaSyAmkmpUG4mxuuUWA2D_XWjNRoATHRA8IlQ';

export default axios.create({
    baseURL: 'https://youtube.googleapis.com/youtube/v3/',
    params: {
        part: 'snippet',
        maxResults: 5,
        key: KEY
    }
})
