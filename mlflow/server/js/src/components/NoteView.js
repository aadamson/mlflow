import React, { Component } from 'react';
import Button from 'react-bootstrap/lib/Button';
import ReactMde from 'react-mde';
import { Converter } from "showdown";
import PropTypes from 'prop-types';
import { setTagApi } from '../Actions';
import { NoteInfo, NOTE_TAG_PREFIX } from "../utils/NoteUtils";
import 'react-mde/lib/styles/css/react-mde-all.css';
import './NoteView.css';

class ShowNoteView extends Component {
  constructor(props) {
    super(props);
    this.renderNote = this.renderNote.bind(this);
    this.handleSubmitClick = this.handleSubmitClick.bind(this);
    this.converter = new Converter({tables: true, simplifiedAutoLink: true});
    this.uneditedContent = this.getUneditedContent();
    this.state = {
      mdeState: undefined,
    };
  }

  static propTypes = {
    runUuid: PropTypes.string.isRequired,
    noteInfo: PropTypes.instanceOf(NoteInfo),
    submitCallback: PropTypes.func.isRequired,
  };

  getUneditedContent() {
    return this.props.noteInfo === undefined ? '' : this.props.noteInfo.content;
  }

  componentWillMount() {
    this.renderNote();
  }

  componentDidUpdate(prevProps) {
    if (this.props.noteInfo !== prevProps.noteInfo || this.props.runUuid !== prevProps.runUuid) {
      this.fetchNotes();
    }
  }

  handleMdeValueChange = (mdeState) => {
    this.setState({ mdeState });
  };

  handleSubmitClick() {
    const self = this;
    const submittedContent = this.state.mdeState.markdown;

    const action = setTagApi(this.props.runUuid, NOTE_TAG_PREFIX + 'content', submittedContent);
    action.payload.then(
      () => {
        self.setState({
          noteInfo: new NoteInfo(submittedContent),
        });
        self.props.submitCallback(submittedContent, undefined);
      },
      (error) => {
        self.props.submitCallback(submittedContent, error);
      }
    );
  }

  contentHasChanged() {
    return this.state.mdeState.markdown !== this.uneditedContent;
  }

  render() {
    const canSubmit = this.contentHasChanged() && !this.state.loading;
    return (
      <div className="note-view-outer-container">
        <div className="text-area-border-box">
          <ReactMde
            layout="tabbed"
            onChange={this.handleMdeValueChange}
            editorState={this.state.mdeState}
            generateMarkdownPreview={markdown => Promise.resolve(this.converter.makeHtml(markdown))}
          />
        </div>
        <div className="submit-button">
          <Button bsStyle="primary"
                  onClick={this.handleSubmitClick}
                  {...(canSubmit ? { active: true } : { disabled: true })}>
            Submit
          </Button>
        </div>
      </div>
    );
  }

  renderNote() {
    this.setState(
      {
        mdeState: {
          markdown: this.uneditedContent
        },
      }
    );
  }
}

export default ShowNoteView;
