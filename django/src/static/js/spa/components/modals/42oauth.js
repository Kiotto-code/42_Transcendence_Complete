import { Component } from '../component.js';

export class Oauth42 extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/modal/oauth42-modal';
		}
	}

	initComponent() {
		super.initComponent();
	}

	cleanupComponent() {
		super.cleanupComponent();
	}

	template() {
		return `
			<div>
				<h1>Modal</h1>
			</div>
		`;
	}
}
