import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity("testentity")
export class TestEntity {
    @PrimaryGeneratedColumn()
	id?: number;

	@Column({ nullable: false, type: "varchar" })
    value!: string;
}
