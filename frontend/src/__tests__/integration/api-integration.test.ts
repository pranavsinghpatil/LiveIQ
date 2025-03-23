import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/auth';
import type { ChatLog, User, ImportChatRequest } from '../../types';

// Create a mock for axios
const mockAxios = new MockAdapter(axios);

describe('API Integration Tests', () => {
  beforeEach(() => {
    useAuthStore.setState({ token: null, user: null });
    mockAxios.reset();
  });

  describe('Authentication', () => {
    it('should login successfully with valid credentials', async () => {
      const mockUser: User = {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
        role: 'user',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      mockAxios.onPost('/auth/login').reply(200, {
        user: mockUser,
        token: 'test-token'
      });

      const response = await api.post('/auth/login', {
        email: 'test@example.com',
        password: 'password123'
      });

      expect(response.status).toBe(200);
      expect(response.data.user).toEqual(mockUser);
      expect(response.data.token).toBeDefined();
    });

    it('should handle guest user limits', async () => {
      const mockGuest: User = {
        id: '2',
        username: 'guest',
        email: 'guest@example.com',
        role: 'guest',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      useAuthStore.setState({ token: 'guest-token', user: mockGuest });

      const importRequest: ImportChatRequest = {
        platform: 'chatgpt',
        content: 'test chat content',
        title: 'Test Chat'
      };

      // First import should succeed
      mockAxios.onPost('/chats/import').reply(200, {
        id: '1',
        title: importRequest.title,
        platform: importRequest.platform
      });
      const response1 = await api.post('/chats/import', importRequest);
      expect(response1.status).toBe(200);

      // Second import should succeed
      mockAxios.onPost('/chats/import').reply(200, {
        id: '2',
        title: importRequest.title,
        platform: importRequest.platform
      });
      const response2 = await api.post('/chats/import', importRequest);
      expect(response2.status).toBe(200);

      // Third import should fail
      mockAxios.onPost('/chats/import').reply(403, {
        error: 'Guest user limit exceeded'
      });
      await expect(api.post('/chats/import', importRequest)).rejects.toThrow();
    });
  });

  describe('Chat Management', () => {
    const mockChat: ChatLog = {
      id: '1',
      title: 'Test Chat',
      platform: 'chatgpt',
      messages: [
        {
          id: '1',
          role: 'user',
          content: 'Hello',
          timestamp: new Date().toISOString()
        }
      ],
      tags: ['test'],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      userId: '1'
    };

    beforeEach(() => {
      useAuthStore.setState({
        token: 'test-token',
        user: {
          id: '1',
          username: 'testuser',
          email: 'test@example.com',
          role: 'user',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      });
    });

    it('should fetch chats successfully', async () => {
      mockAxios.onGet('/chats').reply(200, [mockChat]);
      const response = await api.get('/chats');
      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });

    it('should import chat successfully', async () => {
      const importRequest: ImportChatRequest = {
        platform: 'chatgpt',
        content: 'test chat content',
        title: 'Test Chat',
        tags: ['test']
      };

      mockAxios.onPost('/chats/import').reply(200, {
        id: '1',
        title: importRequest.title,
        platform: importRequest.platform
      });
      const response = await api.post('/chats/import', importRequest);
      expect(response.status).toBe(200);
      expect(response.data).toMatchObject({
        id: expect.any(String),
        title: importRequest.title,
        platform: importRequest.platform
      });
    });

    it('should update chat successfully', async () => {
      const updatedTags = ['test', 'updated'];
      mockAxios.onPatch(`/chats/${mockChat.id}`).reply(200, {
        id: mockChat.id,
        title: mockChat.title,
        platform: mockChat.platform,
        tags: updatedTags
      });
      const response = await api.patch(`/chats/${mockChat.id}`, {
        tags: updatedTags
      });

      expect(response.status).toBe(200);
      expect(response.data.tags).toEqual(updatedTags);
    });

    it('should delete chat successfully', async () => {
      mockAxios.onDelete(`/chats/${mockChat.id}`).reply(200);
      const response = await api.delete(`/chats/${mockChat.id}`);
      expect(response.status).toBe(200);
    });
  });
});
