# ChatSynth Database and Security Design

## Overview

This document outlines the database architecture and security measures implemented in ChatSynth, ensuring data integrity, performance, and user privacy across all platforms and features.

## 1. Database Architecture

### 1.1 Core Schema

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    settings JSONB,
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Chat Logs
CREATE TABLE chat_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    source VARCHAR(50),  -- 'chatgpt', 'claude', 'gemini', etc.
    title VARCHAR(255),
    content JSONB,
    summary TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB,
    is_hybrid BOOLEAN DEFAULT FALSE
);

-- Chat Versions
CREATE TABLE chat_versions (
    id UUID PRIMARY KEY,
    chat_id UUID REFERENCES chat_logs(id),
    version_number INTEGER,
    content JSONB,
    created_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    change_description TEXT
);

-- Annotations
CREATE TABLE annotations (
    id UUID PRIMARY KEY,
    chat_id UUID REFERENCES chat_logs(id),
    user_id UUID REFERENCES users(id),
    content TEXT,
    context JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    position JSONB  -- Stores position within chat
);

-- Tags
CREATE TABLE tags (
    id UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP
);

-- Chat Tags
CREATE TABLE chat_tags (
    chat_id UUID REFERENCES chat_logs(id),
    tag_id UUID REFERENCES tags(id),
    added_by UUID REFERENCES users(id),
    added_at TIMESTAMP,
    PRIMARY KEY (chat_id, tag_id)
);
```

### 1.2 Performance Optimizations

1. **Indexes**
   ```sql
   -- GIN index for JSON content search
   CREATE INDEX idx_chat_logs_content ON chat_logs USING GIN (content jsonb_path_ops);
   
   -- B-tree indexes for common queries
   CREATE INDEX idx_chat_logs_user_id ON chat_logs(user_id);
   CREATE INDEX idx_chat_logs_source ON chat_logs(source);
   CREATE INDEX idx_annotations_chat_id ON annotations(chat_id);
   
   -- Composite indexes for frequent access patterns
   CREATE INDEX idx_chat_tags_composite ON chat_tags(chat_id, tag_id);
   CREATE INDEX idx_chat_versions_chat_version ON chat_versions(chat_id, version_number);
   ```

2. **Partitioning Strategy**
   ```sql
   -- Partition chat_logs by date
   CREATE TABLE chat_logs_partition OF chat_logs
   PARTITION BY RANGE (created_at);
   
   -- Create monthly partitions
   CREATE TABLE chat_logs_y2025m01 
   PARTITION OF chat_logs_partition
   FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
   ```

### 1.3 Data Types and Constraints

1. **Custom Types**
   ```sql
   -- Chat source enum
   CREATE TYPE chat_source AS ENUM (
       'chatgpt',
       'claude',
       'gemini',
       'custom'
   );
   
   -- Content format enum
   CREATE TYPE content_format AS ENUM (
       'text',
       'markdown',
       'html',
       'json'
   );
   ```

2. **Check Constraints**
   ```sql
   -- Add constraints to chat_logs
   ALTER TABLE chat_logs
   ADD CONSTRAINT valid_source 
   CHECK (source = ANY(ARRAY['chatgpt', 'claude', 'gemini', 'custom'])),
   ADD CONSTRAINT valid_content
   CHECK (jsonb_typeof(content) = 'object');
   ```

## 2. Security Implementation

### 2.1 Authentication System

1. **Password Management**
   ```typescript
   interface PasswordPolicy {
       minLength: number;
       requireUppercase: boolean;
       requireNumbers: boolean;
       requireSpecial: boolean;
       maxAge: number;  // days
   }
   
   class PasswordManager {
       async hashPassword(password: string): Promise<string> {
           const salt = await bcrypt.genSalt(12);
           return bcrypt.hash(password, salt);
       }
   
       async verifyPassword(
           password: string, 
           hash: string
       ): Promise<boolean> {
           return bcrypt.compare(password, hash);
       }
   }
   ```

2. **Session Management**
   ```typescript
   interface Session {
       id: string;
       userId: string;
       created: number;
       expires: number;
       metadata: {
           ip: string;
           userAgent: string;
           lastActivity: number;
       };
   }
   
   class SessionManager {
       async createSession(
           userId: string, 
           metadata: any
       ): Promise<Session> {
           // Generate session
           const session = {
               id: uuid(),
               userId,
               created: Date.now(),
               expires: Date.now() + SESSION_DURATION,
               metadata
           };
   
           // Store in Redis
           await this.redis.setex(
               `session:${session.id}`,
               SESSION_DURATION / 1000,
               JSON.stringify(session)
           );
   
           return session;
       }
   }
   ```

### 2.2 Access Control

1. **Role-Based Access Control (RBAC)**
   ```sql
   CREATE TABLE roles (
       id UUID PRIMARY KEY,
       name VARCHAR(50) UNIQUE,
       permissions JSONB
   );
   
   CREATE TABLE user_roles (
       user_id UUID REFERENCES users(id),
       role_id UUID REFERENCES roles(id),
       granted_at TIMESTAMP,
       granted_by UUID REFERENCES users(id),
       PRIMARY KEY (user_id, role_id)
   );
   ```

2. **Permission System**
   ```typescript
   interface Permission {
       resource: string;
       action: 'create' | 'read' | 'update' | 'delete';
       conditions?: {
           ownership?: boolean;
           timeRestriction?: {
               start: number;
               end: number;
           };
       };
   }
   
   class PermissionChecker {
       async checkPermission(
           userId: string,
           resource: string,
           action: string
       ): Promise<boolean> {
           // Get user roles
           const roles = await this.getUserRoles(userId);
           
           // Check permissions
           return this.evaluatePermissions(roles, resource, action);
       }
   }
   ```

### 2.3 Data Encryption

1. **At-Rest Encryption**
   ```typescript
   interface EncryptionConfig {
       algorithm: string;
       keySize: number;
       ivSize: number;
       keyRotationPeriod: number;
   }
   
   class DataEncryptor {
       async encrypt(data: any): Promise<EncryptedData> {
           const iv = crypto.randomBytes(16);
           const key = await this.getLatestKey();
           
           const cipher = crypto.createCipheriv(
               'aes-256-gcm', 
               key, 
               iv
           );
           
           return {
               data: cipher.update(data),
               iv: iv.toString('hex'),
               tag: cipher.getAuthTag()
           };
       }
   }
   ```

2. **In-Transit Encryption**
   ```typescript
   interface TLSConfig {
       version: string;
       ciphers: string[];
       certificatePath: string;
       keyPath: string;
   }
   ```

### 2.4 Audit Logging

1. **Audit Trail**
   ```sql
   CREATE TABLE audit_logs (
       id UUID PRIMARY KEY,
       user_id UUID REFERENCES users(id),
       action VARCHAR(50),
       resource_type VARCHAR(50),
       resource_id UUID,
       metadata JSONB,
       ip_address INET,
       user_agent TEXT,
       created_at TIMESTAMP
   );
   ```

2. **Monitoring System**
   ```typescript
   interface AuditEvent {
       type: 'security' | 'data' | 'access';
       severity: 'info' | 'warning' | 'critical';
       details: {
           user: string;
           action: string;
           resource: string;
           result: string;
           metadata: Record<string, any>;
       };
   }
   ```

## 3. Data Privacy

### 3.1 User Data Protection

1. **Data Classification**
   ```typescript
   enum DataSensitivity {
       PUBLIC = 'public',
       INTERNAL = 'internal',
       CONFIDENTIAL = 'confidential',
       RESTRICTED = 'restricted'
   }
   
   interface DataPolicy {
       sensitivity: DataSensitivity;
       retention: number;  // days
       encryption: boolean;
       accessControl: string[];
   }
   ```

2. **Privacy Settings**
   ```typescript
   interface PrivacySettings {
       dataSharing: {
           analytics: boolean;
           thirdParty: boolean;
           improvement: boolean;
       };
       retention: {
           chatHistory: number;  // days
           analytics: number;    // days
           logs: number;        // days
       };
       export: {
           format: string[];
           includeMeta: boolean;
       };
   }
   ```

### 3.2 Data Retention

1. **Retention Policy**
   ```sql
   -- Retention policy table
   CREATE TABLE retention_policies (
       resource_type VARCHAR(50) PRIMARY KEY,
       retention_period INTERVAL,
       archive_period INTERVAL,
       deletion_strategy VARCHAR(50)
   );
   
   -- Cleanup job
   CREATE OR REPLACE FUNCTION cleanup_expired_data()
   RETURNS void AS $$
   BEGIN
       -- Delete expired chat logs
       DELETE FROM chat_logs
       WHERE created_at < NOW() - 
           (SELECT retention_period 
            FROM retention_policies 
            WHERE resource_type = 'chat_logs');
   END;
   $$ LANGUAGE plpgsql;
   ```

2. **Archival System**
   ```typescript
   interface ArchiveConfig {
       type: 'chat' | 'annotation' | 'audit';
       format: 'json' | 'csv' | 'parquet';
       compression: boolean;
       encryption: boolean;
       storage: 's3' | 'gcs' | 'azure';
   }
   ```

## 4. Performance Monitoring

### 4.1 Query Performance

1. **Query Monitoring**
   ```sql
   -- Create extension for query analysis
   CREATE EXTENSION pg_stat_statements;
   
   -- Query performance view
   CREATE VIEW query_stats AS
   SELECT 
       query,
       calls,
       total_time / calls as avg_time,
       rows / calls as avg_rows
   FROM pg_stat_statements
   ORDER BY total_time DESC;
   ```

2. **Index Usage**
   ```sql
   -- Index usage statistics
   SELECT 
       schemaname,
       tablename,
       indexname,
       idx_scan,
       idx_tup_read,
       idx_tup_fetch
   FROM pg_stat_user_indexes;
   ```

### 4.2 System Metrics

1. **Performance Metrics**
   ```typescript
   interface DatabaseMetrics {
       connections: {
           active: number;
           idle: number;
           max: number;
       };
       performance: {
           queryTime: number;
           ioWait: number;
           cacheHitRatio: number;
       };
       storage: {
           totalSize: number;
           availableSize: number;
           tableGrowth: Record<string, number>;
       };
   }
   ```

2. **Alerting System**
   ```typescript
   interface AlertConfig {
       metric: string;
       threshold: number;
       duration: number;
       severity: 'warning' | 'critical';
       notification: {
           channels: string[];
           message: string;
       };
   }
   ```

## 5. Backup and Recovery

### 5.1 Backup Strategy

1. **Backup Configuration**
   ```typescript
   interface BackupConfig {
       schedule: {
           full: string;     // cron expression
           incremental: string;
           log: string;
       };
       retention: {
           full: number;     // days
           incremental: number;
           log: number;
       };
       storage: {
           primary: string;
           replica: string;
           archive: string;
       };
   }
   ```

2. **Recovery Procedures**
   ```typescript
   interface RecoveryPlan {
       priority: number;
       rpo: number;         // Recovery Point Objective
       rto: number;         // Recovery Time Objective
       steps: {
           order: number;
           action: string;
           duration: number;
       }[];
   }
   ```

## 6. Future Enhancements

### 6.1 Scalability

1. **Horizontal Scaling**
   - Read replicas
   - Sharding strategy
   - Connection pooling
   - Load balancing

2. **Vertical Scaling**
   - Resource optimization
   - Query optimization
   - Index optimization
   - Cache strategy

### 6.2 Advanced Features

1. **Analytics Integration**
   - Real-time analytics
   - Usage patterns
   - Performance metrics
   - User behavior

2. **AI Enhancement**
   - Smart indexing
   - Query prediction
   - Automated optimization
   - Pattern detection
