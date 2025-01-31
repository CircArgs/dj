import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import fetchMock from 'jest-fetch-mock';
import userEvent from '@testing-library/user-event';
import {
  initializeMockDJClient,
  renderCreateNode,
  renderEditNode,
  testElement,
} from './index.test';
import { mocks } from '../../../../mocks/mockNodes';
import { render } from '../../../../setupTests';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import DJClientContext from '../../../providers/djclient';
import { AddEditNodePage } from '../index';

describe('AddEditNodePage submission succeeded', () => {
  beforeEach(() => {
    fetchMock.resetMocks();
    jest.clearAllMocks();
    window.scrollTo = jest.fn();
  });

  it('for creating a node', async () => {
    const mockDjClient = initializeMockDJClient();
    mockDjClient.DataJunctionAPI.createNode.mockReturnValue({
      status: 500,
      json: { message: 'Some columns in the primary key [] were not found' },
    });

    const element = testElement(mockDjClient);
    const { container } = renderCreateNode(element);

    await userEvent.type(
      screen.getByLabelText('Display Name'),
      'Some Test Metric',
    );
    await userEvent.type(screen.getByLabelText('Query'), 'SELECT * FROM test');
    await userEvent.click(screen.getByText('Create dimension'));

    await waitFor(() => {
      expect(mockDjClient.DataJunctionAPI.createNode).toBeCalled();
      expect(mockDjClient.DataJunctionAPI.createNode).toBeCalledWith(
        'dimension',
        'default.some_test_metric',
        'Some Test Metric',
        '',
        'SELECT * FROM test',
        'draft',
        'default',
        null,
      );
      expect(
        screen.getByText(/Some columns in the primary key \[] were not found/),
      ).toBeInTheDocument();
    });

    // After failed creation, it should return a failure message
    expect(container.getElementsByClassName('alert')).toMatchSnapshot();
  }, 60000);

  it('for editing a node', async () => {
    const mockDjClient = initializeMockDJClient();

    mockDjClient.DataJunctionAPI.node.mockReturnValue(mocks.mockMetricNode);
    mockDjClient.DataJunctionAPI.patchNode = jest.fn();
    mockDjClient.DataJunctionAPI.patchNode.mockReturnValue({
      status: 201,
      json: { name: 'default.num_repair_orders', type: 'metric' },
    });

    const element = testElement(mockDjClient);
    renderEditNode(element);

    await userEvent.type(screen.getByLabelText('Display Name'), '!!!');
    await userEvent.type(screen.getByLabelText('Description'), '!!!');
    await userEvent.click(screen.getByText('Save'));

    await waitFor(async () => {
      expect(mockDjClient.DataJunctionAPI.patchNode).toBeCalledTimes(1);
      expect(mockDjClient.DataJunctionAPI.patchNode).toBeCalledWith(
        'default.num_repair_orders',
        'Default: Num Repair Orders!!!',
        'Number of repair orders!!!',
        'SELECT count(repair_order_id) default_DOT_num_repair_orders FROM default.repair_orders',
        'published',
        ['repair_order_id', 'country'],
      );
      expect(
        await screen.getByDisplayValue('repair_order_id, country'),
      ).toBeInTheDocument();
      expect(
        await screen.getByText(/Successfully updated metric node/),
      ).toBeInTheDocument();
    });
  }, 1000000);
});
